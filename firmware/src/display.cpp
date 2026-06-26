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
#define TOUCH_ADDR 0x15

void displayInit() {
  tft.init();
  tft.invertDisplay(true);
  tft.setRotation(0);
  Wire.begin(5, 6);  // SDA=D4(GPIO5), SCL=D5(GPIO6)
  pinMode(TOUCH_INT, INPUT_PULLUP);
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

bool touchRead(int& x, int& y) {
  if (digitalRead(TOUCH_INT) != LOW) return false;
  Wire.beginTransmission(TOUCH_ADDR);
  Wire.write(0x01);  // start od GestureID
  if (Wire.endTransmission(false) != 0) return false;
  Wire.requestFrom(TOUCH_ADDR, 6);
  if (Wire.available() < 6) return false;
  Wire.read();  // gesture
  uint8_t fingers = Wire.read();
  if (fingers == 0) return false;
  uint8_t xh = Wire.read(), xl = Wire.read();
  uint8_t yh = Wire.read(), yl = Wire.read();
  x = ((xh & 0x0F) << 8) | xl;
  y = ((yh & 0x0F) << 8) | yl;
  return true;
}
