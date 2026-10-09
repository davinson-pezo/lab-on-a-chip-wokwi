/**
 * @file config.h
 * @brief System configuration, hardware pinout, and analytical thresholds
 */

#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// --- PINOUT DEFINITIONS ---
#define PIN_BTN_START      2    // External interrupt 0 (Active LOW with internal pull-up)
#define PIN_BTN_STOP       3    // External interrupt 1 (Active LOW with internal pull-up)
#define PIN_STEPPER_DIR    4    // A4988 Direction pin
#define PIN_STEPPER_STEP   5    // A4988 Step pulse pin
#define PIN_VALVE_ACTUATOR 6    // Injection valve (LOW = Load, HIGH = Inject)
#define PIN_LED_RUN        7    // Status LED: Run active (Green)
#define PIN_LED_BUSY       8    // Status LED: Busy / Calibrating (Yellow)
#define PIN_STEPPER_ENABLE 9    // A4988 Enable pin (Active LOW)
#define PIN_CHIP_INJ       10   // Trigger signal to Wokwi Custom Chip
#define PIN_DETECTOR_ADC   A0   // Analog input from Custom Chip UV-Vis detector

// --- OLED DISPLAY CONFIG ---
#define SCREEN_WIDTH       128
#define SCREEN_HEIGHT      64
#define OLED_RESET         -1
#define OLED_I2C_ADDRESS   0x3C

// --- TIMING CONSTANTS ---
#define SAMPLING_PERIOD_MS 40   // 25 Hz ADC sampling (every 40 ms)
#define CALIBRATION_TIME_MS 3000 // 3 seconds baseline auto-zero
#define TOTAL_RUN_TIME_MS  35000 // 35 seconds chromatographic elution run
#define STEPPER_INTERVAL_US 2500 // Step pulse every 2.5 ms (400 Hz = steady flow)

// --- DSP & ANALYTICAL THRESHOLDS ---
#define EMA_ALPHA          0.20f  // Filter smoothing factor (0.0 < alpha <= 1.0)
#define PEAK_START_SLOPE   0.06f  // dV/dt threshold to trigger Peak Start [V/s]
#define PEAK_END_SLOPE     0.02f  // dV/dt threshold to confirm return to baseline
#define PEAK_MIN_HEIGHT    0.20f  // Minimum height above baseline to validate a true peak [V]
#define MAX_DETECTED_PEAKS 4

// --- SYSTEM STATES ---
enum SystemState {
  STATE_IDLE,
  STATE_BASELINE_CAL,
  STATE_INJECT,
  STATE_ELUTION,
  STATE_REPORT
};

// --- DATA STRUCTURE FOR DETECTED CHROMATOGRAPHIC PEAKS ---
struct ChromatographicPeak {
  float retention_time_s;  // tR in seconds
  float start_time_s;      // t_start
  float end_time_s;        // t_end
  float apex_voltage;      // Peak maximum voltage [V]
  float peak_height;       // Height above baseline [V]
  float area;              // Integrated area [V * s]
  float width_s;           // Base width W = t_end - t_start
  float theoretical_plates;// N = 16 * (tR / W)^2
};

#endif // CONFIG_H
