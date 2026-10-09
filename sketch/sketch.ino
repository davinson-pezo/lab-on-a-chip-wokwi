/**
 * @file sketch.ino
 * @brief Standalone Wokwi-ready sketch for Virtual Micro-HPLC & FIA System
 * 
 * Paste this directly into the Wokwi Web "sketch.ino" tab.
 */

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

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

// --- HARDWARE INSTANCES ---
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// --- GLOBAL SYSTEM VARIABLES ---
SystemState current_state = STATE_IDLE;
bool pump_enabled = false;

// Stepper timing
unsigned long last_step_time_us = 0;
bool step_pin_state = false;

// ADC & DSP timing
unsigned long last_sample_time_ms = 0;
unsigned long state_timer_ms = 0;
unsigned long run_start_time_ms = 0;

// Analytical variables
float v_baseline = 0.50f;
float baseline_sum = 0.0f;
uint16_t baseline_samples = 0;

float v_raw = 0.0f;
float v_filtered = 0.50f;
float v_prev_filtered = 0.50f;
float slope_dv_dt = 0.0f;

// Peak detection state
bool tracking_peak = false;
ChromatographicPeak active_peak;
ChromatographicPeak detected_peaks[MAX_DETECTED_PEAKS];
uint8_t peak_count = 0;

// Button debounce
unsigned long last_btn_press_ms = 0;

// --- FORWARD DECLARATIONS ---
void setup_hardware();
void handle_inputs();
void update_fsm();
void update_stepper();
void process_analog_sample();
void update_oled();
void send_serial_telemetry(float t_sec);
void send_final_report();
float calculate_resolution();

// --- SETUP ---
void setup() {
  Serial.begin(115200);
  while (!Serial && millis() < 1000);

  Serial.println(F("\n=================================================="));
  Serial.println(F(" LAB-ON-A-CHIP: VIRTUAL MICRO-HPLC INSTRUMENT"));
  Serial.println(F(" Firmware v2.0 - Antigravity Autonomous LOC Team"));
  Serial.println(F("=================================================="));

  setup_hardware();

  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_I2C_ADDRESS)) {
    Serial.println(F("[ERROR] SSD1306 OLED allocation failed!"));
  } else {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(10, 15);
    display.println(F("MICRO-HPLC FIA"));
    display.setCursor(10, 30);
    display.println(F("INSTRUMENT READY"));
    display.setCursor(10, 48);
    display.println(F("Press START [D2]"));
    display.display();
  }

  Serial.println(F("[SYSTEM] Ready. Press START to begin chromatographic run."));
}

// --- MAIN LOOP ---
void loop() {
  handle_inputs();
  update_stepper();
  update_fsm();
}

// --- HARDWARE CONFIGURATION ---
void setup_hardware() {
  pinMode(PIN_BTN_START, INPUT_PULLUP);
  pinMode(PIN_BTN_STOP, INPUT_PULLUP);

  pinMode(PIN_STEPPER_DIR, OUTPUT);
  pinMode(PIN_STEPPER_STEP, OUTPUT);
  pinMode(PIN_STEPPER_ENABLE, OUTPUT);

  pinMode(PIN_VALVE_ACTUATOR, OUTPUT);
  pinMode(PIN_LED_RUN, OUTPUT);
  pinMode(PIN_LED_BUSY, OUTPUT);
  pinMode(PIN_CHIP_INJ, OUTPUT);

  // Initial actuator states
  digitalWrite(PIN_STEPPER_DIR, HIGH); // Forward rotation
  digitalWrite(PIN_STEPPER_STEP, LOW);
  digitalWrite(PIN_STEPPER_ENABLE, HIGH); // Disabled by default (active LOW)
  digitalWrite(PIN_VALVE_ACTUATOR, LOW);  // Valve in LOAD position
  digitalWrite(PIN_LED_RUN, LOW);
  digitalWrite(PIN_LED_BUSY, LOW);
  digitalWrite(PIN_CHIP_INJ, LOW);
}

// --- USER INPUT HANDLING ---
void handle_inputs() {
  unsigned long now = millis();
  if (now - last_btn_press_ms < 250) return; // Debounce window

  if (digitalRead(PIN_BTN_START) == LOW) {
    last_btn_press_ms = now;
    if (current_state == STATE_IDLE || current_state == STATE_REPORT) {
      Serial.println(F("[USER] START button pressed. Initiating baseline calibration..."));
      current_state = STATE_BASELINE_CAL;
      state_timer_ms = now;
      baseline_sum = 0.0f;
      baseline_samples = 0;
      peak_count = 0;
      pump_enabled = true;
      digitalWrite(PIN_STEPPER_ENABLE, LOW); // Enable motor
      digitalWrite(PIN_LED_BUSY, HIGH);
      digitalWrite(PIN_LED_RUN, LOW);
    }
  }

  if (digitalRead(PIN_BTN_STOP) == LOW) {
    last_btn_press_ms = now;
    if (current_state != STATE_IDLE) {
      Serial.println(F("[USER] STOP/ABORT button pressed. Halting run."));
      current_state = STATE_IDLE;
      pump_enabled = false;
      digitalWrite(PIN_STEPPER_ENABLE, HIGH); // Disable motor
      digitalWrite(PIN_VALVE_ACTUATOR, LOW);
      digitalWrite(PIN_LED_RUN, LOW);
      digitalWrite(PIN_LED_BUSY, LOW);
      update_oled();
    }
  }
}

// --- STEPPER MOTOR PULSE GENERATOR (NON-BLOCKING) ---
void update_stepper() {
  if (!pump_enabled) return;

  unsigned long now_us = micros();
  if (now_us - last_step_time_us >= STEPPER_INTERVAL_US) {
    last_step_time_us = now_us;
    step_pin_state = !step_pin_state;
    digitalWrite(PIN_STEPPER_STEP, step_pin_state);
  }
}

// --- FINITE STATE MACHINE ---
void update_fsm() {
  unsigned long now = millis();

  switch (current_state) {
    case STATE_IDLE:
      // Standby state
      break;

    case STATE_BASELINE_CAL: {
      // Periodic sampling for baseline stabilization
      if (now - last_sample_time_ms >= SAMPLING_PERIOD_MS) {
        last_sample_time_ms = now;
        float sample_v = analogRead(PIN_DETECTOR_ADC) * (5.0f / 1023.0f);
        baseline_sum += sample_v;
        baseline_samples++;
      }

      if (now - state_timer_ms >= CALIBRATION_TIME_MS) {
        if (baseline_samples > 0) {
          v_baseline = baseline_sum / (float)baseline_samples;
        } else {
          v_baseline = 0.50f;
        }
        v_filtered = v_baseline;
        v_prev_filtered = v_baseline;

        Serial.print(F("[CALIBRATION] Baseline stabilized: "));
        Serial.print(v_baseline, 4);
        Serial.println(F(" V. Switching to INJECTION..."));

        // Transition to INJECT
        current_state = STATE_INJECT;
        state_timer_ms = now;
      }
      break;
    }

    case STATE_INJECT: {
      // Actuate injection valve & trigger custom chip
      digitalWrite(PIN_VALVE_ACTUATOR, HIGH);
      digitalWrite(PIN_CHIP_INJ, HIGH);
      delay(20); // Short pulse to trigger chip
      digitalWrite(PIN_CHIP_INJ, LOW);

      Serial.println(F("[INJECT] Valve switched to INJECT. Pulse sent to Custom Chip."));

      run_start_time_ms = millis();
      last_sample_time_ms = run_start_time_ms;
      current_state = STATE_ELUTION;
      digitalWrite(PIN_LED_RUN, HIGH);
      digitalWrite(PIN_LED_BUSY, LOW);

      // Print CSV header for external plotter
      Serial.println(F("TIME_S,RAW_V,FILTERED_V,BASELINE_V,STATE"));
      break;
    }

    case STATE_ELUTION: {
      if (now - last_sample_time_ms >= SAMPLING_PERIOD_MS) {
        last_sample_time_ms = now;
        process_analog_sample();
      }

      // Check if total elution time reached
      if (now - run_start_time_ms >= TOTAL_RUN_TIME_MS) {
        // Complete any open peak integration
        if (tracking_peak && peak_count < MAX_DETECTED_PEAKS) {
          float t_end = (float)(now - run_start_time_ms) / 1000.0f;
          active_peak.end_time_s = t_end;
          active_peak.width_s = active_peak.end_time_s - active_peak.start_time_s;
          if (active_peak.width_s > 0.4f) {
            active_peak.theoretical_plates = 16.0f * sq(active_peak.retention_time_s / active_peak.width_s);
            detected_peaks[peak_count++] = active_peak;
          }
          tracking_peak = false;
        }

        Serial.println(F("[ELUTION] Run completed. Stopping pump and compiling report..."));
        current_state = STATE_REPORT;
        pump_enabled = false;
        digitalWrite(PIN_STEPPER_ENABLE, HIGH);
        digitalWrite(PIN_VALVE_ACTUATOR, LOW);
        digitalWrite(PIN_LED_RUN, LOW);
        digitalWrite(PIN_LED_BUSY, HIGH);

        send_final_report();
        update_oled();
      }
      break;
    }

    case STATE_REPORT:
      // Stays in report display until user presses START to re-run
      break;
  }
}

// --- SIGNAL PROCESSING, PEAK INTEGRATION & DSP ---
void process_analog_sample() {
  float t_sec = (float)(millis() - run_start_time_ms) / 1000.0f;
  float dt_sec = (float)SAMPLING_PERIOD_MS / 1000.0f;

  // 1. Read ADC and convert to Voltage
  int adc_val = analogRead(PIN_DETECTOR_ADC);
  v_raw = (float)adc_val * (5.0f / 1023.0f);

  // 2. Exponential Moving Average (EMA) low-pass filter
  v_filtered = (EMA_ALPHA * v_raw) + ((1.0f - EMA_ALPHA) * v_prev_filtered);

  // 3. Slope estimation (first derivative dV/dt in V/s)
  slope_dv_dt = (v_filtered - v_prev_filtered) / dt_sec;

  // Height above baseline
  float net_signal = v_filtered - v_baseline;
  float prev_net_signal = v_prev_filtered - v_baseline;

  // 4. Peak Tracking Logic
  if (!tracking_peak) {
    // Look for peak onset
    if (slope_dv_dt > PEAK_START_SLOPE && net_signal > 0.08f) {
      tracking_peak = true;
      active_peak.start_time_s = t_sec;
      active_peak.retention_time_s = t_sec;
      active_peak.apex_voltage = v_filtered;
      active_peak.peak_height = net_signal;
      active_peak.area = 0.0f;
      Serial.print(F("[DSP] Peak start detected at t = "));
      Serial.print(t_sec, 2);
      Serial.println(F(" s"));
    }
  } else {
    // Inside a chromatographic peak: Integrate area using Trapezoidal Rule
    if (net_signal > 0.0f && prev_net_signal > 0.0f) {
      active_peak.area += 0.5f * (net_signal + prev_net_signal) * dt_sec;
    }

    // Track Apex (maximum voltage)
    if (v_filtered > active_peak.apex_voltage) {
      active_peak.apex_voltage = v_filtered;
      active_peak.peak_height = net_signal;
      active_peak.retention_time_s = t_sec;
    }

    // Check for Peak Termination (return to baseline)
    bool past_apex = (t_sec > active_peak.retention_time_s + 0.6f);
    bool returned_to_base = (net_signal < 0.12f * active_peak.peak_height) || (net_signal < 0.04f);
    bool slope_flat = (fabs(slope_dv_dt) < PEAK_END_SLOPE);

    if (past_apex && (returned_to_base || slope_flat)) {
      active_peak.end_time_s = t_sec;
      active_peak.width_s = active_peak.end_time_s - active_peak.start_time_s;

      // Validate peak significance
      if (active_peak.peak_height >= PEAK_MIN_HEIGHT && active_peak.width_s >= 0.5f) {
        if (peak_count < MAX_DETECTED_PEAKS) {
          // Column efficiency: N = 16 * (tR / W)^2
          active_peak.theoretical_plates = 16.0f * sq(active_peak.retention_time_s / active_peak.width_s);
          detected_peaks[peak_count++] = active_peak;

          Serial.print(F("[DSP] Peak #"));
          Serial.print(peak_count);
          Serial.print(F(" validated: tR = "));
          Serial.print(active_peak.retention_time_s, 2);
          Serial.print(F(" s, Area = "));
          Serial.print(active_peak.area, 3);
          Serial.print(F(" V*s, Plates N = "));
          Serial.println((int)active_peak.theoretical_plates);
        }
      }
      tracking_peak = false;
    }
  }

  // 5. Send real-time data stream
  send_serial_telemetry(t_sec);

  // Update previous sample
  v_prev_filtered = v_filtered;

  // Update OLED periodically (every 200 ms)
  static unsigned long last_oled_refresh = 0;
  if (millis() - last_oled_refresh > 200) {
    last_oled_refresh = millis();
    update_oled();
  }
}

// --- TELEMETRY OUTPUT (CSV FORMAT) ---
void send_serial_telemetry(float t_sec) {
  Serial.print(t_sec, 2);
  Serial.print(',');
  Serial.print(v_raw, 3);
  Serial.print(',');
  Serial.print(v_filtered, 3);
  Serial.print(',');
  Serial.print(v_baseline, 3);
  Serial.print(',');
  Serial.println(current_state);
}

// --- FINAL ANALYTICAL REPORT ---
void send_final_report() {
  Serial.println(F("\n=================================================="));
  Serial.println(F(" CHROMATOGRAPHIC RUN SUMMARY (JSON)"));
  Serial.println(F("=================================================="));

  float rs = calculate_resolution();

  Serial.println(F("{"));
  Serial.print(F("  \"total_time_s\": ")); Serial.print((float)TOTAL_RUN_TIME_MS / 1000.0f, 1); Serial.println(F(","));
  Serial.print(F("  \"baseline_v\": ")); Serial.print(v_baseline, 4); Serial.println(F(","));
  Serial.print(F("  \"peaks_found\": ")); Serial.print(peak_count); Serial.println(F(","));
  Serial.println(F("  \"peaks\": ["));

  for (uint8_t i = 0; i < peak_count; i++) {
    Serial.println(F("    {"));
    Serial.print(F("      \"id\": ")); Serial.print(i + 1); Serial.println(F(","));
    Serial.print(F("      \"retention_time_s\": ")); Serial.print(detected_peaks[i].retention_time_s, 2); Serial.println(F(","));
    Serial.print(F("      \"height_v\": ")); Serial.print(detected_peaks[i].peak_height, 3); Serial.println(F(","));
    Serial.print(F("      \"area_vs\": ")); Serial.print(detected_peaks[i].area, 4); Serial.println(F(","));
    Serial.print(F("      \"width_s\": ")); Serial.print(detected_peaks[i].width_s, 2); Serial.println(F(","));
    Serial.print(F("      \"theoretical_plates_N\": ")); Serial.print((int)detected_peaks[i].theoretical_plates); Serial.println();
    if (i < peak_count - 1) {
      Serial.println(F("    },"));
    } else {
      Serial.println(F("    }"));
    }
  }

  Serial.println(F("  ],"));
  Serial.print(F("  \"resolution_Rs\": ")); Serial.println(rs, 2);
  Serial.println(F("}"));
  Serial.println(F("==================================================\n"));
}

// --- CHROMATOGRAPHIC RESOLUTION (Rs = 2(tR2 - tR1) / (W1 + W2)) ---
float calculate_resolution() {
  if (peak_count < 2) return 0.0f;
  float dt_r = detected_peaks[1].retention_time_s - detected_peaks[0].retention_time_s;
  float sum_w = detected_peaks[0].width_s + detected_peaks[1].width_s;
  if (sum_w <= 0.001f) return 0.0f;
  return (2.0f * dt_r) / sum_w;
}

// --- OLED DISPLAY RENDERER ---
void update_oled() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  if (current_state == STATE_IDLE) {
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println(F("-- MICRO-HPLC (FIA) --"));
    display.setCursor(0, 20);
    display.println(F("Status: STANDBY"));
    display.setCursor(0, 36);
    display.print(F("Base V: "));
    display.print(v_baseline, 2);
    display.println(F(" V"));
    display.setCursor(0, 52);
    display.println(F("-> Press START [D2]"));
  } 
  else if (current_state == STATE_BASELINE_CAL) {
    display.setTextSize(1);
    display.setCursor(0, 5);
    display.println(F("CALIBRATING SENSOR"));
    display.setCursor(0, 25);
    display.println(F("Zeroing baseline..."));
    display.setCursor(0, 45);
    display.print(F("Progress: "));
    unsigned long elapsed = millis() - state_timer_ms;
    display.print((elapsed * 100) / CALIBRATION_TIME_MS);
    display.println(F(" %"));
  }
  else if (current_state == STATE_ELUTION) {
    float t_sec = (float)(millis() - run_start_time_ms) / 1000.0f;
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print(F("RUN: "));
    display.print(t_sec, 1);
    display.print(F("s / "));
    display.print((float)TOTAL_RUN_TIME_MS / 1000.0f, 0);
    display.println(F("s"));

    display.setCursor(0, 16);
    display.print(F("Det: "));
    display.print(v_filtered, 2);
    display.print(F("V (Net:"));
    display.print(v_filtered - v_baseline, 2);
    display.println(F(")"));

    // Real-time signal level bar
    int bar_width = map((int)(v_filtered * 100), 0, 500, 0, 126);
    display.drawRect(0, 30, 128, 8, SSD1306_WHITE);
    display.fillRect(1, 31, constrain(bar_width, 0, 126), 6, SSD1306_WHITE);

    display.setCursor(0, 46);
    display.print(F("Peaks Detected: "));
    display.println(peak_count);
    if (tracking_peak) {
      display.setCursor(0, 56);
      display.println(F(">> INTEGRATING PEAK <<"));
    }
  }
  else if (current_state == STATE_REPORT) {
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println(F("=== RUN COMPLETE ==="));

    if (peak_count >= 1) {
      display.setCursor(0, 14);
      display.print(F("P1: tR="));
      display.print(detected_peaks[0].retention_time_s, 1);
      display.print(F("s A="));
      display.print(detected_peaks[0].area, 1);
    }
    if (peak_count >= 2) {
      display.setCursor(0, 26);
      display.print(F("P2: tR="));
      display.print(detected_peaks[1].retention_time_s, 1);
      display.print(F("s A="));
      display.print(detected_peaks[1].area, 1);

      display.setCursor(0, 38);
      display.print(F("Resol. Rs: "));
      display.println(calculate_resolution(), 2);
    } else {
      display.setCursor(0, 26);
      display.println(F("Single peak resolved"));
    }

    display.setCursor(0, 52);
    display.println(F("Press START to re-run"));
  }

  display.display();
}
