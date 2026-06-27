#include "camera.h"
#include "esp_camera.h"
#include <Arduino.h>

// Piny kamery OV3660 na Seeed XIAO ESP32-S3 Sense (FPC connector)
#define CAM_PWDN   -1
#define CAM_RESET  -1
#define CAM_XCLK   10
#define CAM_SIOD   40
#define CAM_SIOC   39
#define CAM_Y9     48
#define CAM_Y8     11
#define CAM_Y7     12
#define CAM_Y6     14
#define CAM_Y5     16
#define CAM_Y4     18
#define CAM_Y3     17
#define CAM_Y2     15
#define CAM_VSYNC  38
#define CAM_HREF   47
#define CAM_PCLK   13

static camera_fb_t* last_fb = nullptr;

bool cameraInit() {
  camera_config_t cfg = {};
  cfg.ledc_channel = LEDC_CHANNEL_0;
  cfg.ledc_timer   = LEDC_TIMER_0;
  cfg.pin_d0       = CAM_Y2;
  cfg.pin_d1       = CAM_Y3;
  cfg.pin_d2       = CAM_Y4;
  cfg.pin_d3       = CAM_Y5;
  cfg.pin_d4       = CAM_Y6;
  cfg.pin_d5       = CAM_Y7;
  cfg.pin_d6       = CAM_Y8;
  cfg.pin_d7       = CAM_Y9;
  cfg.pin_xclk     = CAM_XCLK;
  cfg.pin_pclk     = CAM_PCLK;
  cfg.pin_vsync    = CAM_VSYNC;
  cfg.pin_href     = CAM_HREF;
  cfg.pin_sccb_sda = CAM_SIOD;
  cfg.pin_sccb_scl = CAM_SIOC;
  cfg.pin_pwdn     = CAM_PWDN;
  cfg.pin_reset    = CAM_RESET;
  cfg.xclk_freq_hz = 20000000;
  cfg.pixel_format = PIXFORMAT_JPEG;
  cfg.frame_size   = FRAMESIZE_QVGA;  // 320x240 — wystarczy do twarzy
  cfg.jpeg_quality = 15;
  cfg.fb_count     = 2;
  cfg.fb_location  = CAMERA_FB_IN_PSRAM;
  cfg.grab_mode    = CAMERA_GRAB_WHEN_EMPTY;

  esp_err_t err = esp_camera_init(&cfg);
  if (err != ESP_OK) {
    Serial.printf("[CAM] init blad: 0x%x\n", err);
    return false;
  }
  Serial.println("[CAM] init OK");
  return true;
}

bool cameraCapture(uint8_t** buf, size_t* len) {
  if (last_fb) { esp_camera_fb_return(last_fb); last_fb = nullptr; }
  last_fb = esp_camera_fb_get();
  if (!last_fb) return false;
  *buf = last_fb->buf;
  *len = last_fb->len;
  return true;
}

void cameraFree(uint8_t* buf) {
  (void)buf;
  if (last_fb) { esp_camera_fb_return(last_fb); last_fb = nullptr; }
}
