---
applyTo: "**"
---

# Mordo — Kontekst Zespołu

## Igor

- Nie jest programistą, ma dobrą intuicję logiczną
- Język komunikacji: polski

## Autonomia Claude Code

- Gdy Igor pyta lub prosi o opinię — odpowiedz, nie implementuj. Zmiany rób tylko gdy Igor potwierdzi ("tak", "zrób", "ok") lub wprost napisze żeby coś zrobić
- Gdy wystąpi błąd lub problem — opisz co to jest i zaproponuj rozwiązanie. Czekaj na potwierdzenie przed wprowadzeniem jakiejkolwiek zmiany
- Git: patrz `git-autonomy.md` — commit + push automatycznie po przejętym teście manualnym
- Pytaj tylko gdy decyzja zmienia architekturę lub jest sprzeczność w wymaganiach — rzeczy techniczne rozstrzygaj sam
- Nie twórz plików których nie ma w `project-config.md` bez pytania
- Nie przekraczaj 230 linii w żadnym pliku
- Nie kopiuj wzorców z grAlfabet bez pytania
- Firmware: używaj wyłącznie PlatformIO — nie instaluj bibliotek przez Arduino Library Manager, zawsze przez `lib_deps` w `platformio.ini`
- Firmware build+upload: uruchamiaj sam przez `$USERPROFILE/.platformio/penv/Scripts/pio.exe run --target upload` w katalogu `firmware/`. Nie pytaj Igora. Jeśli upload zakończy się błędem zawierającym "No upload ports found" lub "could not open port" — powiedz Igorowi: "podepnij Mordo przez USB do komputera".

## Zasada aktualizacji

Jeśli Igor powie "nie pytaj o to więcej" — natychmiast zaktualizuj odpowiedni plik reguł żeby zasada była zapisana. Nie trzymaj tego tylko w pamięci sesji.
