---
title: "ISSUE-022: Google OAuth setup (Drive API)"
status: planned
type: issue
faza: 2
epic: EPIC-3
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Brain potrafi się uwierzytelnić do Google Drive API w imieniu Igora — jednorazowa autoryzacja
w przeglądarce, potem automatyczne odświeżanie tokenu bez ponownego logowania.

## Acceptance Criteria

- [ ] Projekt w Google Cloud Console z włączonym Drive API (Igor zakłada ręcznie, Claude go przeprowadza)
- [ ] Plik `credentials.json` (OAuth client) pobrany i umieszczony w `brain/` (gitignored)
- [ ] Pierwsze uruchomienie: otwiera się przeglądarka, Igor loguje się i akceptuje dostęp
- [ ] Token zapisywany lokalnie (`brain/data/token.json`, gitignored), automatycznie odświeżany
- [ ] Kolejne uruchomienia brain NIE wymagają ponownego logowania

## Notatki

- Biblioteka: `google-auth-oauthlib` + `google-api-python-client`
- Zakres (scope): `https://www.googleapis.com/auth/drive.file` (dostęp tylko do plików utworzonych
  przez aplikację, nie całego Drive Igora) — bezpieczniejsze niż pełny dostęp
- Ten issue to wyłącznie autoryzacja — żadnego czytania/zapisu zadań jeszcze (to ISSUE-023)
- Zależność: brak (pierwszy krok EPIC-3)

## Test manualny

1. Uruchom skrypt autoryzacyjny → otwiera się przeglądarka, Igor loguje się na Google
2. Po akceptacji → `brain/data/token.json` się tworzy
3. Uruchom ponownie → brak promptu logowania, token się odświeża automatycznie
