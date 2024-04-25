/*
This code was developed by:
    - Miguel Meireles Teixeira, nº 2021217493
    - Damir Ferreira Baspayev Marques, nº 2021218858

Objective: Initial Tests on ESP32 and Servo Motor

This code is available on Github: https://github.com/miguel-mmt2/PL5_Team_1_Repository
*/

// Required Libraries:
#include <ESP32Servo.h>

#define SERVO_PIN 2

Servo servo;

// ============== void setup() ==============
void setup() {
  servo.attach(SERVO_PIN);

  // Default Position is 0º
  servo.write(0);
  delay(1000);     
}

// ============== void loop() ==============
void loop() {
  // 0º -> 180º
  for (int i = 0; i <= 180; i++) {
    servo.write(i);
    delay(20); 
  }

  delay(1000);

  // 180º -> 0
  for (int i = 180; i >= 0; i--) {
    servo.write(i);
    delay(20); 
  }
  delay(1000);
}
