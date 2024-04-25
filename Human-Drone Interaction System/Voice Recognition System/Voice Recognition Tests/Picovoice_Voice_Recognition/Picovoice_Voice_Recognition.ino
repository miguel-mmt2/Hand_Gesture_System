/*
    Copyright 2021-2023 Picovoice Inc.

    You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
    file accompanying this source.

    Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
    an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
    specific language governing permissions and limitations under the License.
*/

#include <Picovoice_EN.h>
#include <string.h>
#include "params.h"

#define BLUE_1 A0
#define GREEN_2 A1
#define RED_1 A2
#define BLUE_2 A3


#define MEMORY_BUFFER_SIZE (70 * 1024)

static const char *ACCESS_KEY = "lDzTVz1FGRVBZDpAIzzNBRCRCZlhCX0/FnDfh+eWVu+yymuRl6oM8w=="; // AccessKey string obtained from Picovoice Console (https://picovoice.ai/console/)

static pv_picovoice_t *handle = NULL;

static int8_t memory_buffer[MEMORY_BUFFER_SIZE] __attribute__((aligned(16)));

static const float PORCUPINE_SENSITIVITY = 0.75f;
static const float RHINO_SENSITIVITY = 0.5f;
static const float RHINO_ENDPOINT_DURATION_SEC = 1.0f;
static const bool RHINO_REQUIRE_ENDPOINT = true;

static void wake_word_callback(void) {
    Serial.println("Wake word detected!");

    digitalWrite(BLUE_1, HIGH);
    digitalWrite(GREEN_2, LOW);
    digitalWrite(RED_1, LOW);
    digitalWrite(BLUE_2, HIGH);
}

static void inference_callback(pv_inference_t *inference) {
    //Serial.print("{");
    //Serial.print("    is_understood : ");
    //Serial.print(inference->is_understood ? "true" : "false");
    if (inference->is_understood) {
        //Serial.print("    intent : ");
        //Serial.print(inference->intent);
        if (inference->num_slots > 0) {
            //Serial.print("    slots : {");
            for (int32_t i = 0; i < inference->num_slots; i++) {
                //Serial.print("        ");
                //Serial.print(inference->slots[i]);
                //Serial.print(" : ");
                //Serial.println(inference->values[i]);
            }
            
            //Serial.print("    }");
            if(strcmp(inference->intent, "changeColor")==0 && strcmp(*inference->slots, "color")==0 && strcmp(*inference->values, "green")==0){
                Serial.println("GREEN");
                digitalWrite(BLUE_1, LOW);
                digitalWrite(GREEN_2, HIGH);
                digitalWrite(RED_1, LOW);
                digitalWrite(BLUE_2, LOW);
            }

            if(strcmp(inference->intent, "changeColor")==0 && strcmp(*inference->slots, "color")==0 && strcmp(*inference->values, "red")==0){
                Serial.println("RED");
                digitalWrite(BLUE_1, LOW);
                digitalWrite(GREEN_2, LOW);
                digitalWrite(RED_1, HIGH);
                digitalWrite(BLUE_2, LOW);
            }
        }
    }




    //Serial.print("}\n");
    pv_inference_delete(inference);
}

static void print_error_message(char **message_stack, int32_t message_stack_depth) {
    for (int32_t i = 0; i < message_stack_depth; i++) {
        Serial.println(message_stack[i]);
    }
}

void setup() {

    pinMode(BLUE_1, OUTPUT);
    pinMode(GREEN_2, OUTPUT);
    pinMode(RED_1, OUTPUT);
    pinMode(BLUE_2, OUTPUT);

    digitalWrite(BLUE_1, LOW);
    digitalWrite(GREEN_2, LOW);
    digitalWrite(RED_1, LOW);
    digitalWrite(BLUE_2, LOW);

    Serial.begin(9600);
    //while (!Serial);


    pv_status_t status = pv_audio_rec_init();
    if (status != PV_STATUS_SUCCESS) {
        Serial.print("Audio init failed with ");
        Serial.println(pv_status_to_string(status));
        while (1);
    }

    char **message_stack = NULL;
    int32_t message_stack_depth = 0;
    pv_status_t error_status;

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

        error_status = pv_get_error_stack(&message_stack, &message_stack_depth);
        if (error_status != PV_STATUS_SUCCESS) {
            Serial.println("Unable to get Porcupine error state");
            while (1);
        }
        print_error_message(message_stack, message_stack_depth);
        pv_free_error_stack(message_stack);

        while (1);
    }

    const char *rhino_context = NULL;
    status = pv_picovoice_context_info(handle, &rhino_context);
    if (status != PV_STATUS_SUCCESS) {
        Serial.print("retrieving context info failed with");
        Serial.println(pv_status_to_string(status));
        while (1);
    }
    Serial.println("Wake word: 'hey computer'");
    Serial.println(rhino_context);
}

void loop() {
    const int16_t *buffer = pv_audio_rec_get_new_buffer();
    if (buffer) {
        const pv_status_t status = pv_picovoice_process(handle, buffer);
        if (status != PV_STATUS_SUCCESS) {
            Serial.print("Picovoice process failed with ");
            Serial.println(pv_status_to_string(status));
            char **message_stack = NULL;
            int32_t message_stack_depth = 0;
            pv_get_error_stack(
                &message_stack,
                &message_stack_depth);
            for (int32_t i = 0; i < message_stack_depth; i++) {
                Serial.println(message_stack[i]);
            }
            pv_free_error_stack(message_stack);
            while (1);
        }
    }
}
