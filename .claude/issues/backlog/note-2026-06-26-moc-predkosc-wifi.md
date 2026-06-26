# Pomysł: informacje o mocy i prędkości przez WiFi

Mordo wysyła przez WiFi (do brain lub bezpośrednio) informacje diagnostyczne:
- poziom naładowania baterii / moc
- siła sygnału WiFi (RSSI — `WiFi.RSSI()` na ESP32)
- prędkość połączenia (throughput)

Może być wyświetlane w brain lub na ekranie LCD.

## Kontekst (2026-06-26)
Igor testował Gemini 3.1 Flash Live w przeglądarce na laptopie (mic laptopa + głośniki laptopa):
brak echa, brak self-interruption, odpowiedzi natychmiastowe.
Gemini wskazał WiFi jako możliwą przyczynę gorszej jakości przez ESP32.
RSSI przyda się do diagnozy latencji: czy problem to WiFi czy architektura audio.
