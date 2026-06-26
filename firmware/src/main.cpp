#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include "driver/i2s.h"
#include "secrets.h"

// Mikrofon PDM
#define PDM_CLK_PIN    42
#define PDM_DATA_PIN   41
#define MIC_RATE       16000
#define CHUNK_SAMPLES  512
#define CHUNK_BYTES    (CHUNK_SAMPLES * 2)

// Głośnik I2S (MAX98357A)
#define SPK_BCLK       7    // D8
#define SPK_LRCLK      44   // D7
#define SPK_DOUT       43   // D6
#define SPK_RATE       24000

// Ring buffer dla audio z brain → głośnik
#define RING_SIZE      8192
static uint8_t  ring_buf[RING_SIZE];
static int      ring_head = 0;
static int      ring_tail = 0;

static int ring_available() {
  return (ring_head - ring_tail + RING_SIZE) % RING_SIZE;
}

static void ring_write(const uint8_t* data, size_t len) {
  for (size_t i = 0; i < len; i++) {
    ring_buf[ring_head] = data[i];
    ring_head = (ring_head + 1) % RING_SIZE;
    if (ring_head == ring_tail)
      ring_tail = (ring_tail + 1) % RING_SIZE; // overflow: wyrzuć najstarsze
  }
}

static size_t ring_read(uint8_t* out, size_t max_len) {
  size_t n = min((size_t)ring_available(), max_len);
  for (size_t i = 0; i < n; i++) {
    out[i] = ring_buf[ring_tail];
    ring_tail = (ring_tail + 1) % RING_SIZE;
  }
  return n;
}

WebSocketsClient ws;

void onWsEvent(WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED)    Serial.println("[WS] polaczono");
  if (type == WStype_DISCONNECTED) Serial.println("[WS] rozlaczono");
  if (type == WStype_BIN) {
    ring_write(payload, length);
  }
  if (type == WStype_TEXT && strcmp((char*)payload, "STOP") == 0) {
    ring_head = ring_tail = 0;
    i2s_zero_dma_buffer(I2S_NUM_1);
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
  i2s_driver_install(I2S_NUM_0, &cfg, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pins);
}


void setupSpeaker() {
  i2s_config_t cfg = {
    .mode                 = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate          = SPK_RATE,
    .bits_per_sample      = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format       = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags     = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count        = 8,
    .dma_buf_len          = 256,
    .use_apll             = false,
    .tx_desc_auto_clear   = true,
  };
  i2s_pin_config_t pins = {
    .bck_io_num   = SPK_BCLK,
    .ws_io_num    = SPK_LRCLK,
    .data_out_num = SPK_DOUT,
    .data_in_num  = I2S_PIN_NO_CHANGE,
  };
  i2s_driver_install(I2S_NUM_1, &cfg, 0, NULL);
  i2s_set_pin(I2S_NUM_1, &pins);
  i2s_zero_dma_buffer(I2S_NUM_1);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("[WiFi] lacze");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\n[WiFi] OK — " + WiFi.localIP().toString());

  ws.begin(BRAIN_IP, BRAIN_PORT, "/");
  ws.onEvent(onWsEvent);
  ws.setReconnectInterval(3000);

  setupMic();
  setupSpeaker();
  Serial.println("[MIC+SPK] gotowe");
}

static uint8_t spk_chunk[1024];

void loop() {
  ws.loop();
  if (!ws.isConnected()) return;

  // Mikrofon → brain
  int16_t mic_buf[CHUNK_SAMPLES];
  size_t bytes_read = 0;
  i2s_read(I2S_NUM_0, mic_buf, CHUNK_BYTES, &bytes_read, pdMS_TO_TICKS(10));
  if (bytes_read > 0)
    ws.sendBIN((uint8_t*)mic_buf, bytes_read);

  // Brain → głośnik (ring buffer → I2S)
  size_t avail = ring_read(spk_chunk, sizeof(spk_chunk));
  if (avail > 0) {
    size_t written = 0;
    i2s_write(I2S_NUM_1, spk_chunk, avail, &written, pdMS_TO_TICKS(5));
  }
}
