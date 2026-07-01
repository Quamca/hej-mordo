---
title: "ISSUE-003: Wake word 'Hej Mordo'"
status: done
type: issue
faza: 0
epic: EPIC-1
created: 2026-06-25
updated: 2026-07-01
---

## Cel

Mordo nie słucha cały czas — aktywuje się dopiero po usłyszeniu "Hej Mordo", niezależnie od
rozpoznania twarzy (ISSUE-021). Działa jako druga, świadoma ścieżka aktywacji.

## Acceptance Criteria

- [x] Detekcja wake word "Hej Mordo" działa lokalnie (Vosk, offline, bez wysyłania do Gemini)
- [x] Po wykryciu wake word → Mordo aktywuje się i zaczyna słuchać (ta sama sesja co ISSUE-021)
- [x] Bez wake word → Mordo nie reaguje na mowę
- [x] Wake word pomija 30s cooldown po dismissie (świadoma komenda = natychmiastowa reaktywacja)

## Podejście

Model Vosk (`vosk-model-small-pl-0.22`, ~50MB, pobrany do `brain/data/vosk-model-pl/`, gitignored)
transkrybuje ciągle audio z przeglądarki w tle. `ws_server.py` rozsyła każdy chunk audio do wielu
odbiorców (`audio_callbacks`, analogicznie do `frame_callbacks`/`photo_callbacks`) — Gemini (podczas
aktywnej sesji) i `wake_word.py` (zawsze) dostają swoją kopię niezależnie.

Wykrycie frazy triggeruje dokładnie ten sam mechanizm co rozpoznanie twarzy z ISSUE-021
(`gemini_client.signal_wake_word()`), więc cała logika powitania/dismiss/rozmowy jest reużyta.

## Notatki

- Nowy moduł: `brain/wake_word.py` — wątek w tle, Vosk `KaldiRecognizer` na 16kHz PCM
- Dopasowanie frazy: regex `hej\W*(mor\w*|moor\w*)`, nie sztywna lista — mały model Vosk słyszy
  "Mordo" fonetycznie różnie (mordę, mordu, morda, mordoru...), regex łapie warianty
- `signal_wake_word()` (gemini_client.py) różni się od `signal_igor_present()` (ISSUE-021, twarz)
  tym że zeruje `_last_dismiss_ts` — świadoma komenda głosowa pomija cooldown, w przeciwieństwie
  do samej obecności przed kamerą
- Zależność: ISSUE-021 done (reużywa `run_triggered()`/trigger event)

## Problemy i rozwiązania

- **Detekcja niekonsekwentna mimo tej samej wymowy**: mały model Vosk (39M) transkrybuje "Mordo"
  różnie za każdym razem (mordę/mordu/morda/mordoru). Fix: regex zamiast listy dokładnych fraz.
- **Reaktywacja głosem nie działała od razu po dismissie**: pierwsza wersja używała tego samego
  triggera co rozpoznanie twarzy, więc 30s cooldown blokował też świadome "Hej Mordo". Fix: osobna
  funkcja `signal_wake_word()` zerująca cooldown.
- **Znany false-positive**: fraza pasująca do wzorca może przypadkiem wypaść w środku dłuższej,
  niezwiązanej wypowiedzi (np. rozmowa O wake wordzie) i triggerować sesję. Zaakceptowane jako
  rzadki przypadek brzegowy — nie zaostrzano dopasowania (np. wymóg pozycji na początku wypowiedzi).

## Test manualny

1. `cd brain && python main.py` — poczekaj na `[WAKE] nasłuch aktywny`
2. Otwórz `pc_mordo.html`, połącz się (bez patrzenia w kamerę)
3. Powiedz "Hej Mordo" → sesja startuje z powitaniem
4. Powiedz "nie dzięki" → dismiss, cisza
5. Od razu powiedz "Hej Mordo" ponownie → sesja startuje natychmiast, bez czekania 30s
