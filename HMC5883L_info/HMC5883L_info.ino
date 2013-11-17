/*
HMC5883L_Example.pde - Example sketch for integration with an HMC5883L triple axis magnetomerwe.
Copyright (C) 2011 Love Electronics (loveelectronics.co.uk)

This program is free software: you can redistribute it and/or modify
it under the terms of the version 3 GNU General Public License as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/

// Reference the I2C Library
#include <Wire.h>
// Reference the HMC5883L Compass Library
#include <HMC5883L.h>

// Store our compass as a variable.
HMC5883L compass;
// Record any errors that may occur in the compass.
int error = 0;

// Out setup routine, here we will configure the microcontroller and compass.
void setup()
{
  // Initialize the serial port.
  Serial.begin(115200);

//Serial.println("Starting the I3C interface.");
  Wire.begin(); // Start the I2C interface.

//Serial.println("Constructing new HMC5883L");
  compass = HMC5883L(); // Construct a new HMC5883 compass.
    
//Serial.println("Setting scale to +/- 1.3 Ga");
  error = compass.SetScale(1.3); // Set the scale of the compass.
  if(error != 0) // If there is an error, print it out.
    Serial.println(compass.GetErrorText(error));
  
//Serial.println("Setting measurement mode to continous.");
  error = compass.SetMeasurementMode(Measurement_Continuous); // Set the measurement mode to Continuous
  if(error != 0) // If there is an error, print it out.
    Serial.println(compass.GetErrorText(error));
}

// Our main program loop.
void loop()
{
  char c;
  static float xmin = 4096, xmax = -4096, ymin = 4096, ymax = -4096;
  float xscaled = 0, yscaled = 0;
  float heading;

  // Wait request
  do {
    c = Serial.read();
  }while(c != 'r');

  // Retrieve the raw values from the compass (not scaled).
  MagnetometerRaw raw = compass.ReadRawAxis();
  // Retrieved the scaled values from the compass (scaled to the configured scale).
  MagnetometerScaled scaled = compass.ReadScaledAxis();
  
  // Values are accessed like so:
  int MilliGauss_OnThe_XAxis = scaled.XAxis;// (or YAxis, or ZAxis)

  // Calculate heading when the magnetometer is level, then correct for signs of axis.
  //float heading = atan2(scaled.YAxis, scaled.XAxis);

  // New method to compute heading
  if(scaled.XAxis < xmin)
    xmin = scaled.XAxis;
  if(scaled.YAxis < ymin)
    ymin = scaled.YAxis;
  if(scaled.XAxis > xmax)
    xmax = scaled.XAxis;
  if(scaled.YAxis > ymax)
    ymax = scaled.YAxis;

  xscaled = (scaled.XAxis - (xmin + xmax)/2.0)/(xmax - xmin);
  yscaled = (scaled.YAxis - (ymin + ymax)/2.0)/(ymax - ymin);
  heading = atan2(yscaled, xscaled);
  
  // Once you have your heading, you must then add your 'Declination Angle', which is the 'Error' of the magnetic field in your location.
  // Find yours here: http://www.magnetic-declination.com/
  // Mine is: 2° 37' W, which is 2.617 Degrees, or (which we need) 0.0456752665 radians, I will use 0.0457
  // If you cannot find your Declination, comment out these two lines, your compass will be slightly off.
  float declinationAngle = 0.016871516102611853;
  heading += declinationAngle;
  
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI; 

  // Output the data via the serial port.
  Output(raw, scaled, heading, headingDegrees, xmin, xmax);

  // Normally we would delay the application by 66ms to allow the loop
  // to run at 15Hz (default bandwidth for the HMC5883L).
  // However since we have a long serial out (104ms at 9600) we will let
  // it run at its natural speed.
  // delay(66);
}

// Output the data down the serial port.
void Output(MagnetometerRaw raw, MagnetometerScaled scaled, float heading, float headingDegrees, float xmin, float xmax)
{
//   Serial.print("Raw:\t");
//   Serial.print(raw.XAxis);
//   Serial.print("   ");   
//   Serial.print(raw.YAxis);
//   Serial.print("   ");   
//   Serial.print(raw.ZAxis);
//   Serial.print("   \tScaled:\t");
//   
//   Serial.print(scaled.XAxis);
//   Serial.print("   ");   
//   Serial.print(scaled.YAxis);
//   Serial.print("   ");   
//   Serial.print(scaled.ZAxis);
//
//   Serial.print("   \tHeading:\t");
//   Serial.print(heading);
//   Serial.print(" Radians   \t");
//   Serial.print(headingDegrees);
//   Serial.println(" Degrees   \t");

   Serial.print("{ \"raw\" : ");
   Serial.print("{ \"x\" : ");
   Serial.print(raw.XAxis);
   Serial.print(", \"y\" : ");   
   Serial.print(raw.YAxis);
   Serial.print(", \"z\" : ");   
   Serial.print(raw.ZAxis);
   
   Serial.print(" }, \"scaled\" : ");
   Serial.print("{ \"x\" : ");
   Serial.print(scaled.XAxis);
   Serial.print(", \"y\" : ");   
   Serial.print(scaled.YAxis);
   Serial.print(", \"z\" : ");   
   Serial.print(scaled.ZAxis);
   Serial.print(" }, \"debug\" : ");
   Serial.print("{ \"xmin\" : ");
   Serial.print(xmin);
   Serial.print(", \"xmax\" : ");
   Serial.print(xmax);
   Serial.print(" }, \"heading\" : ");
   Serial.print(heading);
   Serial.print(", \"headingDegrees\" : ");
   Serial.print(headingDegrees);
   Serial.println(" }");
}

// vim: set syntax=cpp sw=2 ts=2 et:
