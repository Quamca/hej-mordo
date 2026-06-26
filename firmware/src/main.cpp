#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include "driver/i2s.h"
#include "secrets.h"

#define PDM_CLK_PIN   42
#define PDM_DATA_PIN  41
#define SAMPLE_RATE   16000
#define CHUNK_SAMPLES 512
#define CHUNK_BYTES   (CHUNK_SAMPLES * 2)

WebSocketsClient ws;

void onWsEvent(WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED)    Serial.println("[WS] polaczono");
  if (type == WStype_DISCONNECTED) Serial.println("[WS] rozlaczono");
}

void setupMic() {
  i2s_config_t config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_PDM),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_PCM_SHORT,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = 64,
    .use_apll = false,
  };
  i2s_pin_config_t pins = {
    .mck_io_num   = I2S_PIN_NO_CHANGE,
    .bck_io_num   = I2S_PIN_NO_CHANGE,
    .ws_io_num    = PDM_CLK_PIN,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num  = PDM_DATA_PIN,
  };
  i2s_driver_install(I2S_NUM_0, &config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pins);
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("[WiFi] lacze");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[WiFi] OK — " + WiFi.localIP().toString());

  ws.begin(BRAIN_IP, BRAIN_PORT, "/");
  ws.onEvent(onWsEvent);
  ws.setReconnectInterval(3000);

  setupMic();
  Serial.println("[MIC] gotowy");
}

void loop() {
  ws.loop();
  if (!ws.isConnected()) return;

  int16_t buffer[CHUNK_SAMPLES];
  size_t bytes_read = 0;
  i2s_read(I2S_NUM_0, buffer, CHUNK_BYTES, &bytes_read, portMAX_DELAY);

  if (bytes_read > 0) {
    ws.sendBIN((uint8_t*)buffer, bytes_read);
  }
}
