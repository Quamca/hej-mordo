#pragma once
#include <stddef.h>
#include <stdint.h>

bool cameraInit();
// Zwraca wskaźnik na bufor JPEG i jego rozmiar. Wywołaj cameraFree() po użyciu.
bool cameraCapture(uint8_t** buf, size_t* len);
void cameraFree(uint8_t* buf);
