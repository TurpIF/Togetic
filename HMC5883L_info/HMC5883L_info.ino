#include <Wire.h>
#include <HMC5883L.h>

static HMC5883L compass;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  compass = HMC5883L();
  compass.SetMeasurementMode(Measurement_Continuous);
}

void loop() {
  while(Serial.read() != 'r');
  MagnetometerRaw raw = compass.ReadRawAxis();
  Serial.print(raw.XAxis);
  Serial.print(" ");
  Serial.print(raw.YAxis);
  Serial.print(" ");
  Serial.println(raw.ZAxis);
  // delay(66);
}

// vim: set syntax=cpp sw=2 ts=2 et:
