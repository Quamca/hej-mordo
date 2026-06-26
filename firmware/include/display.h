#pragma once

enum MordoState  { MORDO_IDLE, MORDO_LISTEN, MORDO_SPEAK };
enum MordoView   { VIEW_MAIN, VIEW_WIFI };
enum Gesture     { GESTURE_NONE, GESTURE_SWIPE_LEFT, GESTURE_SWIPE_RIGHT };

void displayInit();
void drawStatus(MordoState state);
void drawWifiView(int rssi, const char* ssid);
Gesture gestureRead();
