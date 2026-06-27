---
title: "ISSUE-015: Rozpoznawanie twarzy Igora w brain → ekran ESP32"
status: planned
type: issue
faza: 1
epic: EPIC-2
created: 2026-06-27
updated: 2026-06-27
---

## Cel

Brain rozpoznaje twarz Igora w klatkach z kamery ESP32 i wysyła wynik do ESP32 — ekran pokazuje "siema mordo" gdy Igor zostanie rozpoznany.

## Acceptance Criteria

- [ ] Referencyjne zdjęcie twarzy Igora zapisane w brain (np. `brain/data/igor_face.jpg`)
- [ ] Brain przetwarza klatki z kamery i wykrywa twarz Igora (face_recognition library)
- [ ] Po rozpoznaniu brain wysyła `STATE:face` do ESP32 przez WebSocket
- [ ] Ekran ESP32 wyświetla "siema" na zielonym tle gdy `STATE:face`
- [ ] Gdy twarz znika przez >3s → powrót do normalnego stanu IDLE/LISTEN/SPEAK
- [ ] Nieznana twarz lub brak twarzy → brak zmiany stanu

## Notatki

- Biblioteka: `face_recognition` (dlib wrapper) — pip install face-recognition
- Referencja twarzy: jeden dobry portret Igora wystarczy
- Throttle: nie sprawdzaj każdej klatki — co 5. klatka (oszczędność CPU)
- Zależność: ISSUE-014 musi być done

## Test manualny

1. Uruchom brain i firmware (po ISSUE-014)
2. Stań przed kamerą ESP32 → ekran pokazuje "siema"
3. Odsuń się / zakryj twarz → ekran wraca do stanu poprzedniego
4. Pokaż inne zdjęcie na ekranie telefonu → brak "siema"
