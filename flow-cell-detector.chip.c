/**
 * @file chip.c
 * @brief Wokwi Custom Chip: Virtual Flow Cell Detector & Chromatographic Column
 * 
 * Simulates a micro-HPLC or Flow Injection Analysis (FIA) UV-Vis detector cell.
 * Upon receiving a trigger signal on the INJ pin (indicating sample injection),
 * it generates an analog absorbance profile on AOUT with:
 *   - Continuous baseline voltage (~0.50 V) with slight drift
 *   - Realistic pseudo-random Gaussian noise (thermal/optical noise, ~8 mV RMS)
 *   - Peak 1 (e.g. Theobromine): tR = 12.0 s, Amp = 1.80 V, sigma = 1.2 s
 *   - Peak 2 (e.g. Caffeine):    tR = 25.0 s, Amp = 2.40 V, sigma = 1.8 s
 */

#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct {
  pin_t pin_vcc;
  pin_t pin_gnd;
  pin_t pin_inj;
  pin_t pin_step;
  pin_t pin_aout;
  timer_t update_timer;

  bool running;
  uint64_t start_time_ns;

  // Baseline and thermal drift
  float baseline_v;
  float drift_rate; // V per second

  // Peak 1 parameters (Theobromine)
  float t_r1;
  float amp1;
  float sigma1;

  // Peak 2 parameters (Caffeine)
  float t_r2;
  float amp2;
  float sigma2;

  // Pseudo-random generator state
  uint32_t rng_state;
} flow_cell_detector_t;

// Fast linear congruential generator for pseudo-random numbers
static float random_uniform(uint32_t *state) {
  *state = (*state * 1664525u + 1013904223u);
  return ((float)(*state >> 16) / 65535.0f);
}

// Box-Muller transform for standard Gaussian distributed noise
static float random_gaussian(uint32_t *state, float mean, float stddev) {
  float u1 = random_uniform(state);
  float u2 = random_uniform(state);
  if (u1 < 1e-7f) u1 = 1e-7f;
  float z0 = sqrtf(-2.0f * logf(u1)) * cosf(2.0f * (float)M_PI * u2);
  return mean + (z0 * stddev);
}

// Triggered when the Arduino signals an injection (rising edge on INJ)
static void on_inj_change(void *user_data, pin_t pin, uint32_t value) {
  flow_cell_detector_t *chip = (flow_cell_detector_t *)user_data;
  if (value == HIGH) {
    chip->running = true;
    chip->start_time_ns = get_sim_nanos();
    printf("[CHIP:flow-cell-detector] Sample Injected! Elution clock started at %llu ns.\n", 
           (unsigned long long)chip->start_time_ns);
  }
}

// Periodic timer callback (100 Hz / every 10 ms) to update analog DAC output
static void on_timer_tick(void *user_data) {
  flow_cell_detector_t *chip = (flow_cell_detector_t *)user_data;
  float v_out = chip->baseline_v;

  if (chip->running) {
    uint64_t now_ns = get_sim_nanos();
    float elapsed_s = (float)(now_ns - chip->start_time_ns) / 1.0e9f;

    // Linear baseline drift: ~ +0.5 mV / second
    v_out += (chip->drift_rate * elapsed_s);

    // Peak 1: Gaussian elution profile
    float diff1 = elapsed_s - chip->t_r1;
    float peak1 = chip->amp1 * expf(-(diff1 * diff1) / (2.0f * chip->sigma1 * chip->sigma1));

    // Peak 2: Gaussian elution profile
    float diff2 = elapsed_s - chip->t_r2;
    float peak2 = chip->amp2 * expf(-(diff2 * diff2) / (2.0f * chip->sigma2 * chip->sigma2));

    v_out += (peak1 + peak2);

    // After 40 seconds, the run is complete; keep the baseline
    if (elapsed_s > 40.0f) {
      chip->running = false;
      printf("[CHIP:flow-cell-detector] Elution run finished.\n");
    }
  }

  // Realistic optical/electronic noise (~8 mV standard deviation)
  float noise = random_gaussian(&chip->rng_state, 0.0f, 0.008f);
  v_out += noise;

  // Clamp output voltage safely within the 0.0V to 5.0V range
  if (v_out < 0.0f) v_out = 0.0f;
  if (v_out > 5.0f) v_out = 5.0f;

  pin_dac_write(chip->pin_aout, v_out);
}

void chip_init(void) {
  flow_cell_detector_t *chip = (flow_cell_detector_t *)malloc(sizeof(flow_cell_detector_t));
  if (!chip) {
    printf("[CHIP:flow-cell-detector] Error allocating memory!\n");
    return;
  }

  chip->pin_vcc  = pin_init("VCC", INPUT);
  chip->pin_gnd  = pin_init("GND", INPUT);
  chip->pin_inj  = pin_init("INJ", INPUT_PULLDOWN);
  chip->pin_step = pin_init("STEP", INPUT);
  chip->pin_aout = pin_init("AOUT", ANALOG);

  chip->running = false;
  chip->start_time_ns = 0;
  chip->baseline_v = 0.50f;
  chip->drift_rate = 0.0005f; // +0.5 mV per second

  // Theobromine (tR = 12 s, Peak = 1.8 V, Width = 4.8 s)
  chip->t_r1 = 12.0f;
  chip->amp1 = 1.80f;
  chip->sigma1 = 1.20f;

  // Caffeine (tR = 25 s, Peak = 2.4 V, Width = 7.2 s)
  chip->t_r2 = 25.0f;
  chip->amp2 = 2.40f;
  chip->sigma2 = 1.80f;

  // Seed random generator
  chip->rng_state = 0xABCD1234;

  // Watch for injection pulse
  const pin_watch_config_t watch_inj = {
    .edge = RISING,
    .pin_change = on_inj_change,
    .user_data = chip
  };
  pin_watch(chip->pin_inj, &watch_inj);

  // Setup periodic 10 ms (100 Hz) update timer
  const timer_config_t timer_cfg = {
    .callback = on_timer_tick,
    .user_data = chip
  };
  chip->update_timer = timer_init(&timer_cfg);
  timer_start(chip->update_timer, 10000, true);

  // Initial baseline output
  pin_dac_write(chip->pin_aout, chip->baseline_v);
  printf("[CHIP:flow-cell-detector] Initialized successfully. Base voltage = 0.50 V.\n");
}
