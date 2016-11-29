/*
#Copyright (C) 2016, Juan Pablo Alvarez Galan jpag_erv95@hotmail.com &  Luis Germán Ruelas Luna gruelas@cieco.unam.mx

#This file is part or GeoSat Viewer

#GeoSat Viewer is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Tested in Arduino Uno and Arduino Nano

Arduino code, requires the following sensors:
BMP085 Vcc to 3.3v, SCL to A5, SDA to A4 and GND to ground
DHT11 vcc to 5v, GND to ground and data to D8
GPS Neo6 Vcc to 5v, GND to ground, RX to D4 and TX to D3
Xbee pro S3B Vcc to 3.3v, GND to ground, RX to D10 and TX to D11
A buzzer Vcc to 5v, connected to D9
and a magnetic camp sensor hmc1022 to 5v and A0
*/

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
SoftwareSerial mySerial(3, 4);
SoftwareSerial xbee(10,11);
TinyGPS gps;
int pulso = 6;
int eje = A0;
int x = 0;

void gpsdump(TinyGPS &gps);
void printFloat(double f, int digits = 2);
int speakerOut = 9;
DHT dht(DHTPIN, DHTTYPE);

void setup(){

    pinMode(speakerOut, OUTPUT);
    dht.begin();
    Serial.begin(9600);
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

float a3 = 0.0;
float at[20];
int contador=0;
float a0 = 0;
int altitud_lim = 430;

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
    a3 = bmp.readAltitude();
    if (a3 > a0+altitud_lim){
        Serial.println("Soltando paracaidas!");
        digitalWrite(5,HIGH);
        delay(2000);
        digitalWrite(5,LOW);
        delay(2000);
    }
    xbee.print("1,");
    xbee.print(bmp.readTemperature());
    xbee.print(",");
    xbee.print(bmp.readPressure());
    xbee.print(",");
    xbee.print(a3);
    xbee.println("");

    analogWrite(pulso, 124);
    delay(1000);
    x=analogRead(eje);
    xbee.print("4,");
    xbee.print(x);
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
    
    if(gps.f_altitude()> 1545 + altitud_lim){

        digitalWrite(5,HIGH);
        delay(2000);
        digitalWrite(5,LOW);
        delay(2000);
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
