#pragma once

enum MordoState { MORDO_IDLE, MORDO_LISTEN, MORDO_SPEAK };

void displayInit();
void drawStatus(MordoState state);
bool touchRead(int& x, int& y);
