#include <SPI.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
#include <WiFiNINA.h>
#include "I2Cdev.h"
#include "MPU6050.h"


#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif



char ssid[] = "JApple";        
char password[] = "12345678"; 
 

int status = WL_IDLE_STATUS;   

float latitudeDegrees = 0;
float longitudeDegrees = 0;

MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;

unsigned long previousMillisIMU = 0;
unsigned long previousMillisGPS = 0;
const long intervalIMU = 100;  // 0.1초 (100ms)
const long intervalGPS = 2000; // 2초 (2000ms)
const long intervalBUF = 1000;


IPAddress server(172, 20, 10, 12);    // 서버 주소
String scriptPath = "/data_transfer.php";  // PHP 스크립트 경로



SoftwareSerial mySerial(8, 7);
Adafruit_GPS GPS(&mySerial);
WiFiClient client;

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO  true
#define trigPin 2
#define echoPin 3
#define piezo 11



void setup()
{
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
  #endif






 
  Serial.begin(9600);
  accelgyro.initialize();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(piezo, OUTPUT);

  
  delay(5000);
  Serial.println("Adafruit GPS library basic parsing test!");

  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);

  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time

  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);


  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }


  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, password);
    delay(10000);
  }
  Serial.println("Connected to wifi");




}


void loop()                     // run over and over again
{
   
   unsigned long currentMillis = millis();
   
  
   if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi disconnected. Reconnecting...");
        while (WiFi.status() != WL_CONNECTED) {
            WiFi.begin(ssid, password);
            delay(1000);
        }
        Serial.println("Reconnected to WiFi");
    }
  /*
      long duration, distance;
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 17/1000;

    if(distance < 70){
    // 경보를 출력합니다.
    tone(piezo, 2093);
    delay(10);
    tone(piezo, 523);
    delay(10);
  }

  /// 장애물이 감지 되지 않았다면
  else{
    // 부저를 출력하지 않습니다.
    noTone(piezo);
    // 안전 메세지를 시리얼 모니터에 출력합니다
  }
  */

 

if (currentMillis - previousMillisIMU >= intervalIMU) {
    previousMillisIMU = currentMillis;
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    sendIMUData();            
                        
   
}

 
  // approximately every 2 seconds or so, print out the current stats
  if (currentMillis - previousMillisGPS >= intervalGPS) {
     previousMillisGPS = currentMillis;
   
    char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if ((c) && (GPSECHO))
    Serial.write(c);

  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    //Serial.println(GPS.lastNMEA());   // this also sets the newNMEAreceived() flag to false

    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  
    if (GPS.fix) {

      latitudeDegrees = convertToDecimalDegrees(GPS.latitude, GPS.lat);
      longitudeDegrees = convertToDecimalDegrees(GPS.longitude, GPS.lon);
      Serial.print("Location: ");
      Serial.print(latitudeDegrees, 6);
      Serial.print(", ");
      Serial.print(longitudeDegrees, 6);

      Serial.print(" Speed (knots): "); Serial.println(GPS.speed);
      Serial.print("Angle: "); Serial.println(GPS.angle);
      Serial.print("Altitude: "); Serial.println(GPS.altitude);
      Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
      Serial.print("Antenna status: "); Serial.println((int)GPS.antenna);
    
    
      sendGPSData();
   
    }
   }
 /*
  if (currentMillis - bufferTimer >= intervalBUF) {
        bufferTimer = currentMillis;
        if (imuDataBuffer.length() > 0) {
            sendIMUData();
            imuDataBuffer = ""; // 버퍼 초기화
        }
  }
*/

}


void sendGPSData() {
  if (client.connected()) {
        client.stop(); // 기존 연결이 있는 경우 종료
    }
  
  if (client.connect(server, 80)) {
                String gps_url = "GET " + scriptPath + "?table=gps_data" + "?lat=" + String(latitudeDegrees) + "&lon=" + String(longitudeDegrees) + " HTTP/1.1";
                client.println(gps_url);
                client.println("Host: 127.0.0.1" );
                client.println("Connection: close");
                client.println(); // HTTP 헤더 끝을 의미

                // 서버 응답 읽기
                while (client.connected() || client.available()) {
                    char ch = client.read();
                    Serial.print(ch);
                }
                client.stop();
      }  

}  

void sendIMUData() {
    if (client.connected()) {
        client.stop(); // 기존 연결이 있는 경우 종료
    }

    if (client.connect(server, 80)) {
        String imu_url = "GET " + scriptPath + "?table=imu_data";
        imu_url += "&ax=" + String(ax);
        imu_url += "&ay=" + String(ay);
        imu_url += "&az=" + String(az);
        imu_url += "&gx=" + String(gx);
        imu_url += "&gy=" + String(gy);
        imu_url += "&gz=" + String(gz) + "HTTP/1.1";
        
        
        client.println(imu_url);
        client.println("Host: 127.0.0.1"); // 실제 서버 주소로 변경
        client.println("Connection: close");
        client.println();

        while (client.connected() || client.available()) {
            char ch = client.read();
            Serial.print(ch);
        }
        client.stop();
        delay(20);

    } 

}

float convertToDecimalDegrees(float degreesMinutes, char direction) {
    float degrees = int(degreesMinutes / 100);
    float minutes = degreesMinutes - (degrees * 100);

    float decimalDegrees = degrees + (minutes / 60);
    if (direction == 'S' || direction == 'W') {
        decimalDegrees = -decimalDegrees;  // 남반구나 서반구의 경우 음수로 변환
    }
    return decimalDegrees;
}