---
id: ISSUE-010
title: Latencja i przerywanie odpowiedzi Mordo
status: done
epic: EPIC-2
---

# ISSUE-010: Latencja i przerywanie odpowiedzi Mordo

## Problem

- Mordo zaczyna mówić dopiero gdy Gemini skończy generować całą odpowiedź
- Nie można przerwać Mordo w trakcie mówienia
- VAD czeka ~1s ciszy zanim uzna że skończyłeś mówić

## Acceptance Criteria

- [ ] Mordo zaczyna mówić w ~0.5s od pierwszego chunka audio z Gemini (streaming playback)
- [ ] Gdy Igor mówi podczas odpowiedzi Mordo — Mordo przestaje mówić i słucha (barge-in)
- [ ] VAD silence timeout skrócony do 500ms

## Plan implementacji

### 1. VAD timeout (brain/gemini_client.py)
Dodać do `LiveConnectConfig`:
```python
realtime_input_config=types.RealtimeInputConfig(
    voice_activity_detection=types.VoiceActivityDetection(
        silence_duration_ms=500
    )
)
```

### 2. Streaming playback (brain/audio.py + gemini_client.py)
Zamiast buforować do `turn_complete` i grać naraz:
- Otworzyć `sd.OutputStream` na początku tury
- Wrzucać chunki audio do streamu natychmiast jak przychodzą
- Zamknąć stream po `turn_complete`

### 3. Barge-in / przerywanie (brain/gemini_client.py)
- Usunąć blokadę `if not _is_playing` — zawsze wysyłaj audio do Gemini
- Reagować na `response.server_content.interrupted` — zatrzymać `sd.OutputStream` natychmiast
- Wyczyścić kolejkę audio po przerwaniu

## Pliki do zmiany
| Plik | Zmiana |
|---|---|
| brain/gemini_client.py | VAD config, barge-in, obsługa interrupted |
| brain/audio.py | play_audio → play_stream (OutputStream) |

## Test manualny
1. Mordo zaczyna mówić szybciej niż dotychczas
2. Igor mówi w trakcie odpowiedzi Mordo → Mordo milknie i odpowiada na nowe pytanie
