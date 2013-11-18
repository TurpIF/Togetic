#include <Wire.h>
#include <ADXL345.h>

static ADXL345 accel;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  accel = ADXL345();
  // accel.SetMeasurementMode(Measurement_Continuous);
}

void loop() {
  while(Serial.read(); != 'r');
  AccelerometerRaw raw = accel.ReadRawAxis();
  Serial.print(raw.XAxis);
  Serial.print(" ");
  Serial.print(raw.YAxis);
  Serial.print(" ");
  Serial.println(raw.ZAxis);
  // delay(66);
}

// vim: set syntax=cpp sw=2 ts=2 et:
