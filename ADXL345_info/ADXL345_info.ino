#include <Wire.h>
#include <ADXL345.h>

static ADXL345 accel;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  accel = ADXL345();
  accel.powerOn();
}

void loop() {
  while(Serial.read() != 'r');
  int x, y, z;
  accel.readAccel(&x, &y, &z);
  Serial.print(x);
  Serial.print(" ");
  Serial.print(y);
  Serial.print(" ");
  Serial.println(z);
  // delay(66);
}

// vim: set syntax=cpp sw=2 ts=2 et:
