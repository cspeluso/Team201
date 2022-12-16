#include <TCA9548A.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
//#include <utility/imumaths.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

TCA9548A I2CMux;                  // Address can be passed into the constructor

int IMUS = 8;                     // Number of IMUs being used

void setup() {
  Serial.begin(115200);
  I2CMux.begin(Wire);
  for(uint8_t x = 0; x < IMUS; x++){
    I2CMux.openChannel(x);
    if (!bno.begin()){}
    bno.setExtCrystalUse(true);
    I2CMux.closeChannel(x);
  }
}

void loop() {
  Serial.print(millis());
  for(uint8_t x = 0; x < IMUS; x++){
    I2CMux.openChannel(x);    
    imu::Quaternion quat = bno.getQuat();
    Serial.print(" ");
    Serial.print(quat.w(), 4);
    Serial.print(" ");
    Serial.print(quat.y(), 4);
    Serial.print(" ");
    Serial.print(quat.x(), 4);
    Serial.print(" ");
    Serial.print(quat.z(), 4);
    I2CMux.closeChannel(x);  
  }
  Serial.print('\n');
}