---
title: "ISSUE-021: Auto-trigger Gemini przy rozpoznaniu twarzy + greeting + dismiss"
status: done
type: issue
faza: 0
epic: EPIC-1
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Mordo rozpoznaje Igora → automatycznie startuje sesję Gemini z powitaniem. Jeśli Igor powie "nie dzięki" (lub podobnie) → Gemini kończy sesję i wraca do czekania.

## Podejście

Zamiast zawsze-aktywnej sesji Gemini (jak w ISSUE-019/020), `gemini_client.py` dostał nowy tryb
`run_triggered()` — czeka na sygnał z `face.py` (rozpoznanie twarzy), otwiera sesję z promptem
powitalnym, i zamyka ją gdy model wywoła function call `zakoncz_rozmowe` (dismiss wykrywany przez
sam model, nie przez keyword-matching w brain).

Dwa stany: **IDLE** (brak aktywnej sesji, `face.py` patrzy) i **SESSION** (aktywna rozmowa).
Re-trigger tylko przez wyjście z kadru (≥3s) i powrót, po upływie 30s cooldownu od dismiss.
Wywoływanie głosem w trybie IDLE świadomie NIE wchodzi w zakres tego issue — to ISSUE-003 (wake word),
odłożone na później.

## Acceptance Criteria

- [x] Rozpoznanie Igora triggeruje Gemini (nie czeka na wake word)
- [x] Gemini dostaje system prompt powitalny i sam się odzywa jako pierwszy
- [x] Gemini mówi coś w stylu "cześć, mogę w czymś pomóc?"
- [x] Normalna odpowiedź → kontynuuje rozmowę (wielo-turowa, bez powtórek)
- [x] Dismiss ("nie dzięki" itp.) → Gemini kończy sesję (function call), wraca do nasłuchu twarzy
- [x] Po dismiss — Mordo nie triggeruje ponownie przez 30s (cooldown)
- [x] Jeśli Igor wyjdzie z kadru i wróci (po cooldownie) → trigger odpala się znowu

## Notatki

- `gemini_client.py`: nowa funkcja `run_triggered()` zamiast zawsze-aktywnego `run()`
  - `_greeting_config`: osobny `LiveConnectConfig` z `tools=[FunctionDeclaration("zakoncz_rozmowe")]`
  - Startowa "sztuczna tura": `session.send_client_content(turns=..., turn_complete=True)` zaraz po
    połączeniu — to jedyny sposób żeby Gemini Live odezwał się jako pierwszy, bez czekania na głos
  - Trigger: `asyncio.Event` (`init_trigger()`/`signal_igor_present()`), ustawiany przez `face.py`
    przez `loop.call_soon_threadsafe()` (face.py działa w osobnym wątku)
  - Cooldown: `_last_dismiss_ts` sprawdzany przy każdym triggerze, 30s
- `face.py`: przy rozpoznaniu (przejście `igor_active` False→True) wywołuje dodatkowo `_trigger_gemini()`
- `main.py`: `run_triggered()` zamiast `run()`; dodano `_Tee` — dubluje `print()` do `brain/mordo.log`
  (nadpisywany co start) żeby dało się czytać logi bez kopiowania z terminala

## Problemy i rozwiązania

- **Model witał się w kółko, nawet po realnej odpowiedzi Igora**: przy refaktorze `_receive_audio`
  (dodanie obsługi function-call/dismiss) zgubiona została zewnętrzna pętla `while True` opakowująca
  `async for response in session.receive()`. Gemini Live wymaga ponownego wejścia w `session.receive()`
  dla KAŻDEJ kolejnej tury rozmowy — to nie jest jeden ciągły strumień na całą sesję. Bez tej pętli
  funkcja kończyła się (`return False`) po pierwszej turze, kod nadrzędny brał to za "koniec sesji"
  i łączył się od nowa, wysyłając powitanie ponownie. Diagnoza: dodanie logów per-tura
  (`TURA START`/`TURA KONIEC`/`wysyłam wiadomość startową`) ujawniło wzorzec powtórek bez żadnego
  wyjątku — co wskazało że to nie błąd sieci/API, tylko brakująca pętla.
- **Cichy błąd `send_task` maskował prawdziwą przyczynę**: `asyncio.wait(FIRST_COMPLETED)` sprawdzał
  wynik tylko `recv_task`, nie `send_task` — jakikolwiek wyjątek w wysyłaniu audio ginął bez śladu
  i po cichu triggerował reconnect. Naprawione: sprawdzanie wyjątku obu tasków.
- **Gemini Live nie odzywa się sam z siebie**: samo dodanie instrukcji "przywitaj się" w system
  prompcie nie wystarczy — model czeka na swoją turę. Trzeba wysłać sztuczną wiadomość startową
  przez `send_client_content(turn_complete=True)` zaraz po połączeniu.

## Test manualny

1. `cd brain && python main.py`
2. Otwórz `pc_mordo.html`, połącz się
3. Stań przed kamerą → Gemini wita się sam, jednym zdaniem (bez powtórek)
4. Odpowiedz normalnie → kontynuuje rozmowę
5. Powiedz "nie dzięki" → Gemini żegna się, milknie
6. Zostań przed kamerą — cisza, brak reakcji
7. Odejdź na 30+s i wróć → wita ponownie
