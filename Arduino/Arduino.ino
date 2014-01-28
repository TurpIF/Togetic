#include <Wire.h>
#include <HMC5883L.h>
#include <ADXL345.h>

#define CTRL_REG1 0x20
#define CTRL_REG2 0x21
#define CTRL_REG3 0x22
#define CTRL_REG4 0x23
#define CTRL_REG5 0x24

int L3G4200D_Address = 105; //I2C address of the L3G4200D

void setupGyro() {
  setupL3G4200D(250); // Configure L3G4200  - 250, 500 or 2000 deg/sec
}

void readingGyro(int * x, int * y, int * z) {
  byte xMSB = readRegister(L3G4200D_Address, 0x29);
  byte xLSB = readRegister(L3G4200D_Address, 0x28);
  *x = ((xMSB << 8) | xLSB);

  byte yMSB = readRegister(L3G4200D_Address, 0x2B);
  byte yLSB = readRegister(L3G4200D_Address, 0x2A);
  *y = ((yMSB << 8) | yLSB);

  byte zMSB = readRegister(L3G4200D_Address, 0x2D);
  byte zLSB = readRegister(L3G4200D_Address, 0x2C);
  *z = ((zMSB << 8) | zLSB);
}

int setupL3G4200D(int scale){
  //From  Jim Lindblom of Sparkfun's code

  // Enable x, y, z and turn off power down:
  writeRegister(L3G4200D_Address, CTRL_REG1, 0b00001111);

  // If you'd like to adjust/use the HPF, you can edit the line below to configure CTRL_REG2:
  writeRegister(L3G4200D_Address, CTRL_REG2, 0b00000000);

  // Configure CTRL_REG3 to generate data ready interrupt on INT2
  // No interrupts used on INT1, if you'd like to configure INT1
  // or INT2 otherwise, consult the datasheet:
  writeRegister(L3G4200D_Address, CTRL_REG3, 0b00001000);

  // CTRL_REG4 controls the full-scale range, among other things:

  if(scale == 250) {
    writeRegister(L3G4200D_Address, CTRL_REG4, 0b00000000);
  } else if(scale == 500) {
    writeRegister(L3G4200D_Address, CTRL_REG4, 0b00010000);
  } else {
    writeRegister(L3G4200D_Address, CTRL_REG4, 0b00110000);
  }

  // CTRL_REG5 controls high-pass filtering of outputs, use it
  // if you'd like:
  writeRegister(L3G4200D_Address, CTRL_REG5, 0b00000000);
}

void writeRegister(int deviceAddress, byte address, byte val) {
    Wire.beginTransmission(deviceAddress); // start transmission to device 
    Wire.write(address);       // send register address
    Wire.write(val);         // send value to write
    Wire.endTransmission();     // end transmission
}

int readRegister(int deviceAddress, byte address){
    int v;
    Wire.beginTransmission(deviceAddress);
    Wire.write(address); // register to read
    Wire.endTransmission();

    Wire.requestFrom(deviceAddress, 1); // read a byte
    while(!Wire.available());

    v = Wire.read();
    return v;
}

static HMC5883L compass;
static ADXL345 accel;

void setupAccel() {
  //accel = ADXL345();
  //accel.powerOn();
  accel.begin();
  //accel.setFullResBit(true);
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
  accel.read(x, y, z);
}

void readingCompass(int * x, int * y, int * z) {
  MagnetometerRaw raw = compass.ReadRawAxis();
  *x = raw.XAxis;
  *y = raw.YAxis;
  *z = raw.ZAxis;
}

void output_data(
  int ax, int ay, int az,
  int gx, int gy, int gz,
  int cx, int cy, int cz) {
  String sax = String(ax);
  String say = String(ay);
  String saz = String(az);
  String scx = String(cx);
  String scy = String(cy);
  String scz = String(cz);
  String sgx = String(gx);
  String sgy = String(gy);
  String sgz = String(gz);
  String s =
    sax + " " + say + " " + saz + " " +
    sgx + " " + sgy + " " + sgz + " " +
    scx + " " + scy + " " + scz;
  Serial.println(s);
}

int ax = 0, ay = 0, az = 0;
int gx = 0, gy = 0, gz = 0;
int cx = 0, cy = 0, cz = 0;

void loop() {
  readingAccel(&ax, &ay, &az);
  readingGyro(&gx, &gy, &gz);
  readingCompass(&cx, &cy, &cz);
  if(Serial.available() > 0) {
    if('r' == Serial.read()) {
      output_data(
          ax, ay, az,
          gx, gy, gz,
          cx, cy, cz);
    }
  }

  /*char c = '\0';*/
  /*while(c != 'r') {*/
  /*  c = Serial.read();*/
  /*}*/
  /*int ax = 0, ay = 0, az = 0;*/
  /*int gx = 0, gy = 0, gz = 0;*/
  /*int cx = 0, cy = 0, cz = 0;*/
  /*readingAccel(&ax, &ay, &az);*/
  /*readingGyro(&gx, &gy, &gz);*/
  /*readingCompass(&cx, &cy, &cz);*/
  /*output_data(*/
  /*    ax, ay, az,*/
  /*    gx, gy, gz,*/
  /*    cx, cy, cz);*/
}

// vim: set syntax=cpp sw=2 ts=2 et:
