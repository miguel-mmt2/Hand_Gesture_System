#include <ArduinoBLE.h>
#include <Picovoice_EN.h>
#include <string.h>
#include <Servo.h>

#define GREEN_1 A0
#define GREEN_2 A1
#define RED_1 A2
#define RED_2 A3

#define SERVO_PIN 9 // O pino do servo no ESP32

#define MEMORY_BUFFER_SIZE (70 * 1024)

static const char *ACCESS_KEY = "lDzTVz1FGRVBZDpAIzzNBRCRCZlhCX0/FnDfh+eWVu+yymuRl6oM8w==";

static pv_picovoice_t *handle = NULL;
static int8_t memory_buffer[MEMORY_BUFFER_SIZE] __attribute__((aligned(16)));

BLEService controlService("19B10000-E8F2-537E-4F6C-D104768A1214"); // Service UUID para o controle
BLECharacteristic commandCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite); // Characteristic UUID para os comandos

Servo servo; // Objeto servo

static void wake_word_callback(void) {
    Serial.println("Wake word detected!");
}

static void inference_callback(pv_inference_t *inference) {
    if (inference->is_understood) {
        if(strcmp(inference->intent, "changeColor")==0 && strcmp(*inference->slots, "color")==0 && strcmp(*inference->values, "green")==0){
            Serial.println("GREEN");
            digitalWrite(GREEN_1, HIGH);
            digitalWrite(GREEN_2, HIGH);
            digitalWrite(RED_1, LOW);
            digitalWrite(RED_2, LOW);
            commandCharacteristic.writeValue("GREEN"); // Envie o comando BLE para o ESP32
        }

        if(strcmp(inference->intent, "changeColor")==0 && strcmp(*inference->slots, "color")==0 && strcmp(*inference->values, "red")==0){
            Serial.println("RED");
            digitalWrite(GREEN_1, LOW);
            digitalWrite(GREEN_2, LOW);
            digitalWrite(RED_1, HIGH);
            digitalWrite(RED_2, HIGH);
            commandCharacteristic.writeValue("RED"); // Envie o comando BLE para o ESP32
        }
    }
    pv_inference_delete(inference);
}

void setup() {
    pinMode(GREEN_1, OUTPUT);
    pinMode(GREEN_2, OUTPUT);
    pinMode(RED_1, OUTPUT);
    pinMode(RED_2, OUTPUT);

    digitalWrite(GREEN_1, LOW);
    digitalWrite(GREEN_2, LOW);
    digitalWrite(RED_1, LOW);
    digitalWrite(RED_2, LOW);

    Serial.begin(9600);
    while (!Serial);

    if (!BLE.begin()) {
        Serial.println("starting BLE failed!");
        while (1);
    }

    BLE.setLocalName("NanoBLE33"); // Defina o nome do dispositivo BLE
    BLE.setAdvertisedService(controlService); // Adicione o serviço BLE ao dispositivo
    controlService.addCharacteristic(commandCharacteristic); // Adicione a característica ao serviço
    BLE.addService(controlService); // Adicione o serviço ao dispositivo

    commandCharacteristic.setValue("Waiting for command..."); // Defina um valor inicial para a característica

    pv_status_t status = pv_audio_rec_init();
    if (status != PV_STATUS_SUCCESS) {
        Serial.print("Audio init failed with ");
        Serial.println(pv_status_to_string(status));
        while (1);
    }

    status = pv_picovoice_init(
        ACCESS_KEY,
        MEMORY_BUFFER_SIZE,
        memory_buffer,
        sizeof(KEYWORD_ARRAY),
        KEYWORD_ARRAY,
        PORCUPINE_SENSITIVITY,
        wake_word_callback,
        sizeof(CONTEXT_ARRAY),
        CONTEXT_ARRAY,
        RHINO_SENSITIVITY,
        RHINO_ENDPOINT_DURATION_SEC,
        RHINO_REQUIRE_ENDPOINT,
        inference_callback,
        &handle);
    if (status != PV_STATUS_SUCCESS) {
        Serial.print("Picovoice init failed with ");
        Serial.println(pv_status_to_string(status));
        while (1);
    }

    servo.attach(SERVO_PIN); // Inicialize o servo motor
}

void loop() {
    BLEDevice central = BLE.central();
    if (central) {
        Serial.print("Connected to central: ");
        Serial.println(central.address());

        while (central.connected()) {
            const int16_t *buffer = pv_audio_rec_get_new_buffer();
            if (buffer) {
                const pv_status_t status = pv_picovoice_process(handle, buffer);
                if (status != PV_STATUS_SUCCESS) {
                    Serial.print("Picovoice process failed with ");
                    Serial.println(pv_status_to_string(status));
                    while (1);
                }
            }
        }

        Serial.print("Disconnected from central: ");
        Serial.println(central.address());
    }
}
