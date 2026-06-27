# Auto-start Gemini przy rozpoznaniu twarzy (Faza 3)

Gdy Mordo rozpozna twarz Igora przy biurku → automatycznie odpala sesję Gemini
z kontekstem (kalendarz, lista zadań, nowe maile).

Igor może powiedzieć "nie teraz" lub podobne → Mordo się wyłącza.

Zależności:
- ISSUE-015 (rozpoznawanie twarzy) musi być done
- Faza 2 (pamięć, Google Drive) musi być done
- Faza 3 (mail, kalendarz, triggery)

Docelowo brain może być hostowany na serwerze (działa bez laptopa Igora).
