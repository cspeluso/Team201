// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

//Adjust these as needed, CS_MAX is the length of the Chip-Select array
//CS = chip select, which are the pins that control which IMU (MPU6050) is active
const int CS_MAX = 4;
const int CS[CS_MAX] = {2, 3, 4, 5};
double gyrx_off[CS_MAX];
double gyry_off[CS_MAX];
double gyrz_off[CS_MAX];
int state = 1;

double q[CS_MAX][4];
double angle[3];

const int sampletime = 10; //milliseconds
double Gyr[CS_MAX][3];
double Accel[CS_MAX][3];
unsigned long dt = 0;
int cscount = 0;

double roll[CS_MAX];
double pitch[CS_MAX];
double yaw[CS_MAX];

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {}
  }

  for (int i = 0; i < CS_MAX; i++) {
    pinMode(CS[i], OUTPUT);
    digitalWrite(CS[i], HIGH);
    delay(10);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    break;
  case MPU6050_RANGE_4_G:
    break;
  case MPU6050_RANGE_8_G:
    break;
  case MPU6050_RANGE_16_G:
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    break;
  case MPU6050_RANGE_500_DEG:
    break;
  case MPU6050_RANGE_1000_DEG:
    break;
  case MPU6050_RANGE_2000_DEG:
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_10_HZ);
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    break;
  case MPU6050_BAND_184_HZ:
    break;
  case MPU6050_BAND_94_HZ:
    break;
  case MPU6050_BAND_44_HZ:
    break;
  case MPU6050_BAND_21_HZ:
    break;
  case MPU6050_BAND_10_HZ:
    break;
  case MPU6050_BAND_5_HZ:
    break;
  }

  Serial.println("");
  delay(100);
  
}

void loop() {
  if(state == 1){
    for(int i = 0; i < CS_MAX; i++){
      digitalWrite(CS[i], LOW);
      /*
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);
      //CODE TO DETERMINE BIAS OF GYROSCOPES
      double gyrx = 0;
      double gyry = 0;
      double gyrz = 0;
      int j = 0;
      while(j<100){
        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);
        gyrx += g.gyro.x;
        gyry += g.gyro.y;
        gyrz += g.gyro.z;
        j++;
      }
      Serial.println(gyrx, 4);
      Serial.println(gyry, 4);
      Serial.println(gyrz, 4);
      gyrx_off[i] = gyrx/1000;
      gyry_off[i] = gyry/1000;
      gyrz_off[i] = gyrz/1000;
      Serial.print(gyrx_off[i]);
      Serial.print(", ");
      Serial.print(gyry_off[i]);
      Serial.print(", ");
      Serial.println(gyrz_off[i]);
      */
      digitalWrite(CS[i], HIGH);
    }
    state = 2;
  }else{
    digitalWrite(CS[cscount], LOW);
    /* Get new sensor events with the readings */
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    ///*
    Gyr[cscount][0] = (g.gyro.x - gyrx_off[cscount]) * 180 / 3.1415;
    Gyr[cscount][1] = (g.gyro.y - gyry_off[cscount]) * 180 / 3.1415;
    Gyr[cscount][2] = (g.gyro.z - gyrz_off[cscount]) * 180 / 3.1415;
    //*/
    /*
    Gyr[cscount][0] = g.gyro.x;
    Gyr[cscount][1] = g.gyro.y;
    Gyr[cscount][2] = g.gyro.z;
    */
    /*
    Accel[cscount][0] = a.acceleration.x;
    Accel[cscount][1] = a.acceleration.y;
    Accel[cscount][2] = a.acceleration.z;
    */

    digitalWrite(CS[cscount], HIGH);

    if(cscount == CS_MAX-1){
      dt = micros() - dt;

      //Serial.print(millis());
      //Serial.print(dt);
      //Serial.print(" ");

      for(int i = 0; i < CS_MAX; i++){
        ///*
        roll[i] += Gyr[i][0]*dt/10e6;
        pitch[i] += Gyr[i][1]*dt/10e6;
        yaw[i] += Gyr[i][2]*dt/10e6;
        //*/
        /*
        Serial.print(Gyr[i][0], 4);
        Serial.print(" ");
        Serial.print(Gyr[i][1], 4);
        Serial.print(" ");
        Serial.print(Gyr[i][2], 4);
        Serial.print(" ");
        */
        /*
        Serial.print(roll[i], 4);
        Serial.print(" ");
        Serial.print(pitch[i], 4);
        Serial.print(" ");
        Serial.print(yaw[i], 4);
        Serial.print(" ");
        */
        
        q[i][0] = sin(roll[i]/2) * cos(pitch[i]/2) * cos(yaw[i]/2) - cos(roll[i]/2) * sin(pitch[i]/2) * sin(yaw[i]/2);
        q[i][1] = cos(roll[i]/2) * sin(pitch[i]/2) * cos(yaw[i]/2) + sin(roll[i]/2) * cos(pitch[i]/2) * sin(yaw[i]/2);
        q[i][2] = cos(roll[i]/2) * cos(pitch[i]/2) * sin(yaw[i]/2) - sin(roll[i]/2) * sin(pitch[i]/2) * cos(yaw[i]/2);
        q[i][3] = cos(roll[i]/2) * cos(pitch[i]/2) * cos(yaw[i]/2) + sin(roll[i]/2) * sin(pitch[i]/2) * sin(yaw[i]/2);      
        
      }
      for(int i = 0; i<3; i++){
        
        angle[i] = (180 / 3.1415)*(2*acos(q[i][0]*q[i+1][0]+q[i][1]*q[i+1][1]+q[i][2]*q[i+1][2]+q[i][3]*q[i+1][3]));
        Serial.print("ANGLE BETWEEN IMU ");
        Serial.print(i+1);
        Serial.print(" AND IMU ");
        Serial.print(i+2);
        Serial.print(" IS: ");
        Serial.println(angle[i], 4);
        
      }
      

      Serial.println();
      cscount = -1;
    }

    cscount++;

    dt = micros();

    //delay(samplerate);
  }
}
