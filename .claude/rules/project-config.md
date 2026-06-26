---
applyTo: "**"
---

# Mordo — Konfiguracja Projektu

## Ścieżki

| Zmienna | Wartość |
|---|---|
| `{project}` | katalog główny repozytorium Mordo |
| `{memory}` | `{project}/memory/` — pliki pamięci Mordo (Google Drive sync) |
| `{firmware}` | `{project}/firmware/` — kod ESP32-S3 |
| `{brain}` | `{project}/brain/` — PC-side agent Python |
| `{docs}` | `{project}/docs/` — dokumentacja HTML |
| `{issues}` | `{project}/.claude/issues/` — aktywne zadania |
| `{backlog}` | `{project}/.claude/issues/backlog/` — pomysły nie na teraz |

## Stack techniczny

| Warstwa | Technologia |
|---|---|
| Firmware | Arduino C++ (ESP32-S3) |
| Brain (PC) | Python 3.11+ |
| Głos/AI | Gemini Flash Live API (WebSocket) |
| Pamięć | Google Drive (Google API) |
| Mail/Kalendarz | Gmail + Google Calendar (Google API) |
| Dokumentacja | HTML (statyczne pliki) |
| Testy firmware | manualne na urządzeniu (PlatformIO w VS Code) |
| Testy brain | pytest |

## Hardware (docelowy)

- Seeed Xiao ESP32-S3 Sense (wlutowane piny)
- Kamera OV3660 + taśma FPC 75mm (120°)
- Wyświetlacz Seeed Round Display for XIAO 1.28" 240×240 IPS (model 104030087) — sterownik GC9A01 (SPI), dotyk CHSC6X I2C 0x2e (nie CST816S!), wtyczka bezpośrednio na XIAO
- Wzmacniacz MAX98357A I2S DAC
- Głośnik 8Ω 2W
- Akumulator Li-Pol 4000mAh

## Fazy projektu

| Faza | Opis | Hardware |
|---|---|---|
| 0 — Software Mordo | Gemini Live + głos + rozpoznawanie twarzy + symulacja ekranu — wszystko na laptopie | NIE (laptop) |
| 1 — Hardware Mordo | ESP32 jako terminal sprzętowy (mikrofon, kamera, ekran, głośnik) komunikujący się z brain przez WebSocket; firmware w Arduino C++ | TAK |
| 2 — Pamięć | Dotflow, Google Drive, kontekst między sesjami | TAK |
| 3 — Proaktywny | Mail, kalendarz, triggery, harmonogram | TAK |
| 4 — PC Agenci | Sterowanie komputerem, pliki, dokumentacja HTML | TAK |

Zasada: każda faza musi być stabilna zanim zaczyna się następna.

## Firmware — setup

- Środowisko: PlatformIO w VS Code (nie Arduino IDE)
- Zależności: wyłącznie przez `lib_deps` w `platformio.ini`
- Build: polecenie Build w VS Code (nie ręczna instalacja bibliotek)
- Bazowy `platformio.ini`:
  ```ini
  [env:seeed_xiao_esp32s3]
  platform = espressif32
  board = seeed_xiao_esp32s3
  framework = arduino
  monitor_speed = 115200
  ```

## Referencje

| Projekt | Link | Czego szukać |
|---|---|---|
| OmniBot (nazirlouis) | https://github.com/nazirlouis/OmniBot | Gemini Live API, wake word, rozpoznawanie twarzy, persona, ESP32 — niemal identyczna architektura jak Mordo |

Zasada: referencje służą do nauki i rozwiązywania problemów — nie kopiujemy kodu bez analizy.

### Kiedy sprawdzać OmniBot

Przy nowych issue dotyczących: audio, barge-in, VAD, latencji, Gemini Live protokołu, wake word, rozpoznawania twarzy, osobowości — sprawdź najpierw jak OmniBot to rozwiązał. Często szybciej niż w dokumentacji.

Przydatne pliki:
- `app/backend/gemini_live_session.py` — logika sesji Gemini Live
- `app/backend/wake_listen.py` — VAD, wykrywanie mowy

Znane rozwiązania zaczerpnięte z OmniBot:
- VAD config: `prefix_padding_ms=200, silence_duration_ms=400`
