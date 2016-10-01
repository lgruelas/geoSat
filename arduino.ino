#include <TinyGPS.h>
#include <SoftwareSerial.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>

#define  C     1912    // 523 Hz
#define  R     0
#define DHTPIN 8
#define DHTTYPE DHT11   // DHT 11


Adafruit_BMP085 bmp;
SoftwareSerial mySerial(3, 4); // RX, TX
SoftwareSerial xbee(10,11); // RX, TX
TinyGPS gps;

void gpsdump(TinyGPS &gps);
void printFloat(double f, int digits = 2);
int speakerOut = 9;
DHT dht(DHTPIN, DHTTYPE);

void setup(){

    pinMode(speakerOut, OUTPUT);
    dht.begin();
    xbee.begin(57600);
    mySerial.begin(9600);

    if (!bmp.begin()) {
        xbee.println("Could not find a valid BMP085 sensor, check wiring!");
        while (1) {}
    }
}

int melody[] = { C };
int beats[]  = { 8 };
int MAX_COUNT = sizeof(melody) / 2;
long tempo = 10000;
int pause = 100;
int rest_count = 100;

int tone_ = 0;
int beat = 0;
long duration  = 0;

float a1, a2, a3;
float at[20];
int contador=0;
float a0 = 0;

void playTone() {

    long elapsed_time = 0;
    if (tone_ > 0) { 

        while (elapsed_time < duration) {

            digitalWrite(speakerOut,HIGH);
            delayMicroseconds(tone_ / 2);

            digitalWrite(speakerOut, LOW);
            delayMicroseconds(tone_ / 2);

            elapsed_time += (tone_);
    }
  } else { 

        for (int j = 0; j < rest_count; j++) {
            delayMicroseconds(duration);  
    }                                
  }                                
}

void loop() {
    if (a0 == 0){
        if (contador < 20){
            at[contador] = bmp.readAltitude();
            contador++;
        } else {
            for (int i = 0; i < 20; i++){
                a0+=at[i];
        }
        a0/=20.0;
      }
    } else {
    xbee.print("1,");
    xbee.print(bmp.readTemperature());
    xbee.print(",");
    xbee.print(bmp.readPressure());
    xbee.print(",");
    xbee.print(bmp.readAltitude());
    xbee.println("");
  bool newdata = false;
  unsigned long start = millis();

  while (millis() - start < 250) {
    if (mySerial.available()) {
      char c = mySerial.read();
      if (gps.encode(c)) {
        newdata = true;
      }
    }
  }
  
  if (newdata) {
    gpsdump(gps);
  }
  for (int i=0; i<MAX_COUNT; i++) {
    tone_ = melody[i];
    beat = beats[i];
    
    duration = beat * tempo;
    
    playTone();
    delayMicroseconds(pause);
  }
    float h = dht.readHumidity();
    float t = dht.readTemperature();
  
    if (isnan(h) || isnan(t)) {
      xbee.println("Failed to read from DHT sensor!");
      return;
    }

    xbee.print("3,");
    xbee.print(t);
    xbee.print(",");
    xbee.print(h);
    xbee.println("");
    }
}

void gpsdump(TinyGPS &gps){

    float flat, flon;
    unsigned long age;

    gps.f_get_position(&flat, &flon, &age);
    xbee.print("2,");
    printFloat(flat, 5);
    xbee.print(",");
    printFloat(flon, 5);
    xbee.print(",");
    printFloat(gps.f_altitude());
    xbee.println("");
    
    if(gps.f_altitude()> 1915){

        xbee.println(">1975");
        digitalWrite(5,HIGH);
        delay(2000);
        digitalWrite(5,LOW);
        delay(1000);
    }
}

void printFloat(double number, int digits){

    if (number < 0.0) {
        xbee.print('-');
        number = -number;
    }

    double rounding = 0.5;
    for (uint8_t i=0; i<digits; ++i){
        rounding /= 10.0;
    }
  
    number += rounding;

    unsigned long int_part = (unsigned long)number;
    double remainder = number - (double)int_part;
    xbee.print(int_part);

    if (digits > 0)
        xbee.print("."); 

    while (digits-- > 0) {
        remainder *= 10.0;
        int toPrint = int(remainder);
        xbee.print(toPrint);
        remainder -= toPrint;
    }
}
