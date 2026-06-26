#include <Arduino.h>
#include <driver/i2s.h>
#include <math.h>

#define I2S_NUM         I2S_NUM_0
#define I2S_BCLK        7   // D8
#define I2S_LRCLK       44  // D7
#define I2S_DOUT        43  // D6

#define SAMPLE_RATE     24000
#define TONE_HZ         440
#define AMPLITUDE       8000
#define BUF_SAMPLES     256

static int16_t buf[BUF_SAMPLES * 2]; // stereo
static float phase = 0.0f;
static const float phase_inc = 2.0f * M_PI * TONE_HZ / SAMPLE_RATE;

void setup() {
    Serial.begin(115200);
    Serial.println("[test] I2S speaker init");

    i2s_config_t cfg = {
        .mode                 = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
        .sample_rate          = SAMPLE_RATE,
        .bits_per_sample      = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format       = I2S_CHANNEL_FMT_RIGHT_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags     = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count        = 8,
        .dma_buf_len          = 128,
        .use_apll             = false,
        .tx_desc_auto_clear   = true,
    };

    i2s_pin_config_t pins = {
        .bck_io_num   = I2S_BCLK,
        .ws_io_num    = I2S_LRCLK,
        .data_out_num = I2S_DOUT,
        .data_in_num  = I2S_PIN_NO_CHANGE,
    };

    i2s_driver_install(I2S_NUM, &cfg, 0, NULL);
    i2s_set_pin(I2S_NUM, &pins);
    i2s_zero_dma_buffer(I2S_NUM);

    Serial.println("[test] gramy 440Hz przez 5 sekund...");
}

void loop() {
    for (int i = 0; i < BUF_SAMPLES; i++) {
        int16_t sample = (int16_t)(sinf(phase) * AMPLITUDE);
        buf[i * 2]     = sample; // L
        buf[i * 2 + 1] = sample; // R
        phase += phase_inc;
        if (phase > 2.0f * M_PI) phase -= 2.0f * M_PI;
    }
    size_t written = 0;
    i2s_write(I2S_NUM, buf, sizeof(buf), &written, portMAX_DELAY);
}
