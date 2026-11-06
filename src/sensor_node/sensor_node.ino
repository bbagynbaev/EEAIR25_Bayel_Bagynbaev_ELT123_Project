#include <WiFi.h>
#include <esp_now.h>

const int NODE_ID = 1;

uint8_t hubAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

typedef struct struct_message {
  int id;       
  float pm25;   
  float pm10;   
} struct_message;

struct_message myData;
esp_now_peer_info_t peerInfo;

#define RXD2 16  
#define TXD2 17  

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\n[ESP-NOW] Packet to Hub: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "SUCCESS" : "FAIL");
}

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
  
  Serial.println("\n--- Dust Dispersion Mapper: Sensor Node ---");

  WiFi.mode(WIFI_STA);
  
  if (esp_now_init() != ESP_OK) {
    Serial.println("[ERROR] Failed to initialize ESP-NOW");
    return;
  }
  
  esp_now_register_send_cb(OnDataSent);
  
  memcpy(peerInfo.peer_addr, hubAddress, 6);
  peerInfo.channel = 0;    
  peerInfo.encrypt = false; 
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("[ERROR] Failed to add Hub as peer");
    return;
  }
}

void loop() {
  if (Serial2.available() > 0) {
    uint8_t startByte = Serial2.read();
    
    if (startByte == 0xAA) {
      delay(10); 
      
      if (Serial2.available() >= 9) {
        uint8_t commandByte = Serial2.read();
        
        if (commandByte == 0xC0) {
          uint8_t pm25_low  = Serial2.read();
          uint8_t pm25_high = Serial2.read();
          uint8_t pm10_low  = Serial2.read();
          uint8_t pm10_high = Serial2.read();
          uint8_t id1 = Serial2.read();
          uint8_t id2 = Serial2.read();
          uint8_t checksum = Serial2.read();
          uint8_t tailByte = Serial2.read();

          if (tailByte == 0xAB) {
            float pm25 = ((pm25_high * 256.0) + pm25_low) / 10.0;
            float pm10 = ((pm10_high * 256.0) + pm10_low) / 10.0;

            myData.id = NODE_ID;
            myData.pm25 = pm25;
            myData.pm10 = pm10;

            esp_err_t result = esp_now_send(hubAddress, (uint8_t *) &myData, sizeof(myData));
        
            Serial.printf("Node %d | PM2.5: %.1f ug/m3 | PM10: %.1f ug/m3\n", NODE_ID, pm25, pm10);
          }
        }
      }
    }
  }
}