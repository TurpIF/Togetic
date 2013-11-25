#include <Wire.h>
#include <HMC5883L.h>
#include <ADXL345.h>

static HMC5883L compass;
static ADXL345 accel;

void setupAccel() {
  accel = ADXL345();
  accel.powerOn();
}

void setupGyro() {
  // TODO
}

void setupCompass() {
  compass = HMC5883L();
  compass.SetMeasurementMode(Measurement_Continuous);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  setupAccel();
  setupGyro();
  setupCompass();
  delay(1000);
}

void readingAccel(int * x, int * y, int * z) {
  accel.readAccel(x, y, z);
}

void readingGyro(int * x, int * y, int * z) {
  // TODO
}

void readingCompass(int * x, int * y, int * z) {
  MagnetometerRaw raw = compass.ReadRawAxis();
  *x = raw.XAxis;
  *y = raw.YAxis;
  *z = raw.ZAxis;
}

void loop() {
  char c = '\0';
  while(c != 'a' || c != 'g' || c != 'c')
      c = Serial.read();
  int x, y, z;
  if(c == 'a')
      readingAccel(&x, &y, &z);
  else if(c == 'g')
      readingGyro(&x, &y, &z);
  else
      readingCompass(&x, &y, &z);
  Serial.print(x);
  Serial.print(" ");
  Serial.print(y);
  Serial.print(" ");
  Serial.println(z);
}

// vim: set syntax=cpp sw=2 ts=2 et:
