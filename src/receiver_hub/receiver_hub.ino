#include <WiFi.h>
#include <esp_now.h>

typedef struct struct_message {
  int id;       
  float pm25;   
  float pm10;   
} struct_message;

struct_message myData;

void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));

  Serial.printf("DATA,%d,%.1f,%.1f\n", myData.id, myData.pm25, myData.pm10);
}

void setup() {
  Serial.begin(115200);
  
  Serial.println("\n--- Dust Dispersion Mapper: Central Hub ---");

  WiFi.mode(WIFI_STA);
  
  Serial.print("[INFO] Hub MAC Address: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println("[ERROR] Error initializing ESP-NOW");
    return;
  }
  
  esp_now_register_recv_cb(OnDataRecv);
  Serial.println("[INFO] Hub initialized. Waiting for sensor nodes data...");
}

void loop() {
  delay(1000); 
}