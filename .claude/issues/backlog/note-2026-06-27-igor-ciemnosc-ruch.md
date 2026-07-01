# "Igor?" — detekcja ruchu w ciemności / po 20:00 (Faza 3)

Gdy kamera wyłapie ruch lub człowieka ale nie rozpozna twarzy (za ciemno):

- **Jasno / przed 20:00**: Mordo pyta głosem "czy to ty Igor?"
- **Ciemno / po 20:00**: ekran pokazuje "Igor?" + przyciski TAK/NIE (dotyk)

Wymaga:
- Detekcja ruchu (frame diff lub MediaPipe person detection)
- Logika czasowa (godzina systemowa na brain)
- Przyciski dotykowe na ekranie Round Display (nowy widok display.cpp)
- Zależność: ISSUE-015 (rozpoznawanie twarzy) musi być done
- Faza 3 (proaktywny Mordo)
