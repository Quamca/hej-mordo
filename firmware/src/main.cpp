#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include "driver/i2s.h"
#include "secrets.h"
#include "display.h"
#include "camera.h"

// Mikrofon PDM
#define PDM_CLK_PIN    42
#define PDM_DATA_PIN   41
#define MIC_RATE       16000
#define CHUNK_SAMPLES  512
#define CHUNK_BYTES    (CHUNK_SAMPLES * 2)

// Głośnik I2S — wyłączony (D7/D8 zajęte przez ekran, wróci po relutowaniu)
// #define SPK_BCLK  7   // D8 — konflikt z SPI SCK ekranu
// #define SPK_LRCLK 44  // D7 — konflikt z touch INT ekranu

// Ring buffer dla audio z brain → głośnik (nieaktywny, pins zajęte przez ekran)
#define RING_SIZE 8192
static uint8_t ring_buf[RING_SIZE];
static int ring_head = 0, ring_tail = 0;

static int ring_available() {
  return (ring_head - ring_tail + RING_SIZE) % RING_SIZE;
}
static void ring_write(const uint8_t* data, size_t len) {
  for (size_t i = 0; i < len; i++) {
    ring_buf[ring_head] = data[i];
    ring_head = (ring_head + 1) % RING_SIZE;
    if (ring_head == ring_tail) ring_tail = (ring_tail + 1) % RING_SIZE;
  }
}

WebSocketsClient ws;
static MordoState current_state = MORDO_IDLE;
static MordoView  active_view   = VIEW_MAIN;

void onWsEvent(WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED) {
    Serial.println("[WS] polaczono");
    current_state = MORDO_LISTEN;
    if (active_view == VIEW_MAIN) drawStatus(MORDO_LISTEN);
  }
  if (type == WStype_DISCONNECTED) {
    Serial.println("[WS] rozlaczono");
    current_state = MORDO_IDLE;
    if (active_view == VIEW_MAIN) drawStatus(MORDO_IDLE);
  }
  if (type == WStype_BIN) {
    ring_write(payload, length);  // bufor audio — speaker wyłączony, dane ignorowane
  }
  if (type == WStype_TEXT) {
    char* msg = (char*)payload;
    if (strcmp(msg, "STOP") == 0) {
      ring_head = ring_tail = 0;
    } else if (strncmp(msg, "STATE:", 6) == 0) {
      char* state = msg + 6;
      if      (strcmp(state, "idle")   == 0) current_state = MORDO_IDLE;
      else if (strcmp(state, "listen") == 0) current_state = MORDO_LISTEN;
      else if (strcmp(state, "speak")  == 0) current_state = MORDO_SPEAK;
      if (active_view == VIEW_MAIN) drawStatus(current_state);  // guard: nie nadpisuj widoku WiFi
    }
  }
}

void setupMic() {
  i2s_config_t cfg = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_PDM),
    .sample_rate = MIC_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_PCM_SHORT,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4, .dma_buf_len = 64, .use_apll = false,
  };
  i2s_pin_config_t pins = {
    .mck_io_num = I2S_PIN_NO_CHANGE, .bck_io_num = I2S_PIN_NO_CHANGE,
    .ws_io_num = PDM_CLK_PIN, .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = PDM_DATA_PIN,
  };
  i2s_driver_install(I2S_NUM_0, &cfg, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pins);
}

void setup() {
  Serial.begin(115200);

  displayInit();  // ekran init przed WiFi — pokazuje szary okrąg podczas łączenia

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("[WiFi] lacze");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\n[WiFi] OK — " + WiFi.localIP().toString());

  ws.begin(BRAIN_IP, BRAIN_PORT, "/");
  ws.onEvent(onWsEvent);
  ws.setReconnectInterval(3000);

  setupMic();
  cameraInit();
  Serial.println("[MIC+CAM] gotowe, ekran aktywny");
}


static unsigned long last_cam_ms = 0;
static const uint8_t CAM_HEADER[4] = {'C', 'A', 'M', 0};

void loop() {
  ws.loop();

  // Mikrofon → brain (działa niezależnie od połączenia WS)
  int16_t mic_buf[CHUNK_SAMPLES];
  size_t bytes_read = 0;
  i2s_read(I2S_NUM_0, mic_buf, CHUNK_BYTES, &bytes_read, pdMS_TO_TICKS(10));
  if (bytes_read > 0 && ws.isConnected())
    ws.sendBIN((uint8_t*)mic_buf, bytes_read);

  // Kamera — jedna klatka JPEG co 200ms (5 fps)
  unsigned long now = millis();
  if (ws.isConnected() && now - last_cam_ms >= 200) {
    last_cam_ms = now;
    uint8_t* jpg; size_t jpg_len;
    if (cameraCapture(&jpg, &jpg_len)) {
      // Wyślij: 4B nagłówek CAM\0 + dane JPEG
      size_t total = 4 + jpg_len;
      uint8_t* pkt = (uint8_t*)malloc(total);
      if (pkt) {
        memcpy(pkt, CAM_HEADER, 4);
        memcpy(pkt + 4, jpg, jpg_len);
        ws.sendBIN(pkt, total);
        free(pkt);
      }
      cameraFree(jpg);
    }
  }

  Gesture g = gestureRead();
  if (g == GESTURE_SWIPE_RIGHT && active_view == VIEW_MAIN) {
    active_view = VIEW_WIFI;
    drawWifiView(WiFi.RSSI(), WiFi.SSID().c_str());
  } else if (g == GESTURE_SWIPE_LEFT && active_view == VIEW_WIFI) {
    active_view = VIEW_MAIN;
    drawStatus(current_state);
  }
}
