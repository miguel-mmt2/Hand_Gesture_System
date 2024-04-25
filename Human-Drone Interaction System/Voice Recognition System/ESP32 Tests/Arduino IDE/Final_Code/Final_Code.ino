/*
This code was developed by:
    - Miguel Meireles Teixeira, nº 2021217493
    - Damir Ferreira Baspayev Marques, nº 2021218858

Objective: Final code on WiFi connection between PC and ESP32.

          This code waits the computer to send a message to ESP32. To send a message to ESP32 
          we used the code avilable on our GitHub:

This code is available on Github: https://github.com/miguel-mmt2/PL5_Team_1_Repository
*/

// Required Libraries:
#include <WiFi.h>
#include <ESP32Servo.h>

#define SERVO_PIN 2

// Internet Name and Password
const char* ssid = "Vodafone-16B85B";
const char* password = "VpARFuY9aE";

WiFiServer server(80);

Servo servo;

// ============== void setup() ==============
void setup() {
  servo.attach(SERVO_PIN);
  servo.write(0); 

  Serial.begin(9600);
  delay(10);

  // WiFi connection
  Serial.println();
  Serial.println();
  Serial.print("Conectando à rede ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());

  // Server Initialize
  server.begin();
  Serial.println("Servidor iniciado");
}

// ============== void loop() ==============
void loop() {
  // Waits the client connection
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  // Wait the client to send data
  while (!client.available()) {
    delay(1);
  }

  // Reead the client message
  String message = client.readStringUntil('\r');
  Serial.println("Mensagem recebida: " + message);

  // GREEN
  if(message == "GREEN"){
    for (int i = 0; i <= 180; i++) {
      servo.write(i);
      delay(20); 
    }  
  }

  // RED
  if(message == "RED"){
    for (int i = 180; i >= 0; i++) {
      servo.write(i);
      delay(20); 
    }  
  }

  // Send confirmation to client
  client.println("Mensagem recebida com sucesso!");
  client.flush();
}
