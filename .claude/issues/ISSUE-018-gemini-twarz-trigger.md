---
title: "ISSUE-018: Auto-start Gemini przy rozpoznaniu twarzy + wizja kamery"
status: planned
type: issue
faza: 1
epic: EPIC-2
created: 2026-06-27
updated: 2026-06-27
---

## Cel

Gdy brain rozpozna Igora → automatycznie odpala sesję Gemini Live z promptem powitalnym.
Gemini dostaje klatki z kamery (wizja). Jeśli brak głośnika → odpowiedź tekstem w terminalu.

## Acceptance Criteria

- [ ] Rozpoznanie Igora triggeruje Gemini (nie czeka na wake word)
- [ ] Gemini dostaje system prompt: "Igor jest w zasięgu, przywitaj go i zapytaj czy coś możesz dla niego zrobić"
- [ ] Gemini dostaje klatki kamery (Gemini Live obsługuje wideo przez inline_data JPEG)
- [ ] Brak głośnika → odpowiedź Gemini pojawia się jako tekst w terminalu brain
- [ ] Test: "co widzisz?" → Gemini opisuje obraz z kamery
- [ ] "nie teraz" lub podobne → Mordo kończy sesję i wraca do nasłuchu

## Notatki

- Gemini Live API obsługuje wideo: `session.send_realtime_input(video=types.Blob(data=jpg, mime_type="image/jpeg"))`
- Throttle klatek do Gemini: co 1s (nie 5fps — to zbyt dużo danych)
- Tryb tekstowy: `response_modalities=["TEXT"]` zamiast ["AUDIO"] gdy brak głośnika
- Zależność: ISSUE-015 done ✓
- Kolejność: przed ISSUE-017 (przycisk zdjęć) — ważniejsze

## Test manualny

1. Uruchom `python brain/main.py`
2. Stań przed kamerą → Gemini wita Igora (tekst w terminalu lub głos)
3. Zapytaj "co widzisz?" → Gemini opisuje obraz
4. Powiedz "nie teraz" → Mordo wraca do nasłuchu, ekran IDLE
