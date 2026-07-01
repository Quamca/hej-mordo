---
title: "ISSUE-019: PC audio — rozmowa z Gemini przez mikrofon i głośniki laptopa"
status: in-progress
type: issue
faza: 0
epic: EPIC-1
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Otwierasz `brain/pc_mordo.html` w przeglądarce i możesz rozmawiać z Gemini przez mikrofon i głośniki laptopa.

## Podejście (zmienione w trakcie pracy)

Pierwotny plan (natywne audio przez `sounddevice` w Pythonie, osobny `pc_mordo.py`) porzucony —
kombinacja mikrofon+głośnik+tkinter w wątkach powodowała powtarzalny, twardy crash Windows
(`0xc0000005`/`0xc000001d`, potwierdzone w Event Viewer). Diagnoza opisana w sekcji "Problemy i rozwiązania".

Finalne podejście: **przeglądarka jako klient WebSocket**, dokładnie tak jak ESP32.
Zero zmian w backendzie — `ws_server.py`, `audio.py`, `gemini_client.py`, `main.py` zostały bez zmian.

## Acceptance Criteria

- [x] `main.py` startuje i łączy się z Gemini Live
- [x] Mikrofon laptopa (przez przeglądarkę, `getUserMedia`) wysyła audio do Gemini
- [x] Głośniki laptopa (przez przeglądarkę, Web Audio API) odtwarzają odpowiedź Gemini w czasie rzeczywistym
- [x] Gemini nie przerywa sam siebie (barge-in działa płynnie — Igor może przerywać Gemini)
- [ ] Ctrl+C w `main.py` czysto kończy sesję (do potwierdzenia)

## Notatki

- Nowy plik: `brain/pc_mordo.html` — jeden plik HTML+JS, otwierany bezpośrednio (`file://`), bez serwera HTTP
- Mikrofon: `getUserMedia` + `AudioContext(sampleRate:16000)` + `ScriptProcessorNode` → PCM16 → WebSocket binary
- Głośnik: WebSocket binary (PCM16 24kHz) → `AudioBufferSourceNode`, planowane sekwencyjnie przez `playCursor`
- Sygnały tekstowe z serwera: `STATE:listen` / `STATE:speak` (UI), `STOP` (zatrzymanie odtwarzania — zarówno turn_complete jak i interrupted)
- Ważne: `STOP` musi zatrzymywać WSZYSTKIE zaplanowane źródła audio, nie tylko ostatnie — inaczej bieżący fragment gra do końca mimo przerwania (patrz Problemy i rozwiązania)
- `mic_local.py`, `speaker_local.py`, `pc_mordo.py` (natywny prototyp) — usunięte, zastąpione przez podejście webowe

## Test manualny

1. `cd brain && python main.py`
2. Otwórz `pc_mordo.html` w Chrome, kliknij "Połącz z Mordo", zezwól na mikrofon
3. Powiedz "cześć" → Gemini odpowiada głosem przez głośniki
4. Przerwij Gemini w połowie zdania → Gemini przestaje mówić natychmiast, słucha dalej
5. Ctrl+C w terminalu `main.py` → program kończy bez błędów

## Problemy i rozwiązania

- **Twardy crash Windows (mikrofon+głośnik+tkinter w wątkach)**: `pc_mordo.py` z natywnym audio
  (`sounddevice`) i oknem statusu tkinter crashował ~2-3s po starcie sesji, bez żadnego wyjątku Pythona
  (potwierdzone w Event Viewer: `0xc0000005`/`0xc000001d`, moduł `unknown`). Izolacja przez eliminację
  (mikrofon sam, mikrofon+Gemini, +GUI, +głośnik, w różnych kombinacjach wątków) pokazała że problem
  występuje WYŁĄCZNIE gdy tkinter i prawdziwy głośnik (`sd.OutputStream`) działają jednocześnie —
  każda inna kombinacja (nawet mikrofon+głośnik w wątku w tle, bez GUI) działała bez zarzutu.
  Rozwiązanie: całkowita rezygnacja z tkinter/sounddevice na rzecz przeglądarki.
- **Fałszywe tropy po drodze**: `GEMINI_API_KEY` nieustawiony (okno "znikało" bo program kończył się
  przed utworzeniem GUI), `UnicodeEncodeError` przy przekierowaniu stdout (polskie znaki + cp1252),
  WASAPI/COM na wątku mikrofonu (Intel Smart Sound wymagał `CoInitializeEx` + natywna częstotliwość
  48kHz z resamplingiem software'owym) — te poprawki DZIAŁAŁY, ale nie usuwały głównego crasha.
  Wniosek: warto izolować zmienne pojedynczo zamiast łatać warstwowo, kiedy crash jest twardy i cichy.
- **Opóźnione przerywanie (barge-in)**: w wersji webowej frontend śledził tylko ostatnio zaplanowany
  fragment audio (`currentSource`), więc sygnał `STOP` zatrzymywał niewłaściwy (jeszcze nie odtwarzany)
  fragment, a aktualnie grający leciał do końca. Fix: śledzenie wszystkich zaplanowanych fragmentów
  (`scheduledSources[]`), zatrzymanie wszystkich na `STOP`.
