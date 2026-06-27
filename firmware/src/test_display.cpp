#define LGFX_USE_V1
#include <LovyanGFX.hpp>
#include <Arduino.h>

class LGFX : public lgfx::LGFX_Device {
  lgfx::Panel_GC9A01 _panel;
  lgfx::Bus_SPI _bus;
public:
  LGFX() {
    auto cfgb = _bus.config();
    cfgb.spi_host   = SPI2_HOST;
    cfgb.freq_write = 40000000;
    cfgb.pin_sclk   = 7;
    cfgb.pin_mosi   = 9;
    cfgb.pin_miso   = 8;
    cfgb.pin_dc     = 4;
    _bus.config(cfgb);
    _panel.setBus(&_bus);

    auto cfgp = _panel.config();
    cfgp.pin_cs     = 2;
    cfgp.pin_rst    = -1;
    cfgp.panel_width  = 240;
    cfgp.panel_height = 240;
    _panel.config(cfgp);
    setPanel(&_panel);
  }
};

static LGFX tft;

void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(3, OUTPUT);
  digitalWrite(3, HIGH);  // SD_CS — wyłącz SD z magistrali SPI
  delay(10);

  tft.init();
  tft.invertDisplay(true);
  tft.setRotation(0);
  pinMode(43, OUTPUT);
  digitalWrite(43, HIGH);  // XIAO_BL backlight
}

void loop() {
  Serial.println("[TEST] czerwony");
  tft.fillScreen(TFT_RED);
  delay(1500);

  Serial.println("[TEST] zielony");
  tft.fillScreen(TFT_GREEN);
  delay(1500);

  Serial.println("[TEST] niebieski");
  tft.fillScreen(TFT_BLUE);
  delay(1500);

  Serial.println("[TEST] szary okrag");
  tft.fillScreen(TFT_BLACK);
  tft.fillCircle(120, 120, 108, 0x444444);
  tft.setTextColor(TFT_WHITE, 0x444444);
  tft.setTextDatum(middle_center);
  tft.setFont(&fonts::FreeSansBold12pt7b);
  tft.drawString("...", 120, 120);
  delay(2000);
}
