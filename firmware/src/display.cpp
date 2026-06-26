#define LGFX_USE_V1
#include <LovyanGFX.hpp>
#include <Wire.h>
#include "display.h"

// GC9A01 przez SPI na Seeed Round Display for XIAO
class LGFX : public lgfx::LGFX_Device {
  lgfx::Panel_GC9A01 _panel;
  lgfx::Bus_SPI       _bus;
public:
  LGFX() {
    {
      auto cfg = _bus.config();
      cfg.spi_host   = SPI2_HOST;
      cfg.freq_write = 80000000;
      cfg.pin_sclk   = 7;   // D8
      cfg.pin_mosi   = 9;   // D10
      cfg.pin_miso   = 8;   // D9
      cfg.pin_dc     = 4;   // D3
      _bus.config(cfg);
      _panel.setBus(&_bus);
    }
    {
      auto cfg = _panel.config();
      cfg.pin_cs      = 2;  // D1
      cfg.pin_rst     = -1;
      cfg.panel_width  = 240;
      cfg.panel_height = 240;
      _panel.config(cfg);
    }
    setPanel(&_panel);
  }
};

static LGFX tft;

#define TOUCH_INT  44   // D7
#define TOUCH_ADDR 0x2e // CHSC6X (nie CST816S)

static volatile bool touch_flag   = false;
static unsigned long last_touch_ms = 0;

void IRAM_ATTR touchISR() { touch_flag = true; }

void displayInit() {
  tft.init();
  tft.invertDisplay(true);
  tft.setRotation(0);
  Wire.begin(5, 6);  // SDA=D4(GPIO5), SCL=D5(GPIO6)
  pinMode(TOUCH_INT, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(TOUCH_INT), touchISR, FALLING);
  drawStatus(MORDO_IDLE);
}

void drawStatus(MordoState state) {
  struct { uint32_t bg; const char* text; } cfg[] = {
    { 0x444444, "..."     },  // IDLE
    { 0x0055FF, "slucham" },  // LISTEN
    { 0x00AA44, "mowie"   },  // SPEAK
  };
  tft.fillScreen(TFT_BLACK);
  tft.fillCircle(120, 120, 108, cfg[state].bg);
  tft.setTextColor(TFT_WHITE, cfg[state].bg);
  tft.setTextDatum(middle_center);
  tft.setFont(&fonts::FreeSansBold12pt7b);
  tft.drawString(cfg[state].text, 120, 120);
}

static int  swipe_start_x = -1;
static int  swipe_end_x   = -1;
static bool swipe_active  = false;

static bool touchXRead(int& x) {
  uint8_t buf[5] = {0};
  uint8_t len = Wire.requestFrom(TOUCH_ADDR, (uint8_t)5);
  if (len < 5) return false;
  Wire.readBytes(buf, len);
  if (buf[0] != 0x01) return false;
  x = buf[2];
  return true;
}

Gesture gestureRead() {
  if (touch_flag) {
    touch_flag    = false;
    last_touch_ms = millis();
    int x;
    if (touchXRead(x)) {
      if (!swipe_active) { swipe_start_x = x; swipe_active = true; }
      swipe_end_x = x;
    }
    return GESTURE_NONE;
  }

  // brak nowego pulsu przez >80ms = palec podniesiony
  if (swipe_active && (millis() - last_touch_ms > 80)) {
    swipe_active = false;
    int delta = swipe_end_x - swipe_start_x;
    Serial.printf("[SWIPE] start=%d end=%d delta=%d\n", swipe_start_x, swipe_end_x, delta);
    if (delta >  50) return GESTURE_SWIPE_RIGHT;
    if (delta < -50) return GESTURE_SWIPE_LEFT;
  }
  return GESTURE_NONE;
}

static int rssiToBars(int rssi) {
  if (rssi >= -55) return 4;
  if (rssi >= -67) return 3;
  if (rssi >= -78) return 2;
  if (rssi >= -89) return 1;
  return 0;
}

void drawWifiView(int rssi, const char* ssid) {
  tft.fillScreen(TFT_BLACK);

  // 4 pionowe kreski siły sygnału (wyrównane do środka, rosnąca wysokość)
  int bars     = rssiToBars(rssi);
  int barW     = 18, gap = 10;
  int totalW   = 4 * barW + 3 * gap;
  int startX   = (240 - totalW) / 2;
  int baseY    = 110;
  int maxH     = 52;

  for (int i = 0; i < 4; i++) {
    int h    = 12 + i * (maxH - 12) / 3;
    int x    = startX + i * (barW + gap);
    int y    = baseY - h;
    uint32_t color = (i < bars) ? 0x00DD00 : 0x444444;
    tft.fillRoundRect(x, y, barW, h, 4, color);
  }

  // SSID pod kreskami
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextDatum(middle_center);
  tft.setFont(&fonts::FreeSans9pt7b);
  tft.drawString(ssid, 120, 148);

  // wartość RSSI drobno pod SSID
  char buf[16];
  snprintf(buf, sizeof(buf), "%d dBm", rssi);
  tft.setFont(&fonts::Font2);
  tft.drawString(buf, 120, 170);
}
