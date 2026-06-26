# Długa latencja odpowiedzi Mordo

## Opis
Mordo długo czeka zanim odpowie po wypowiedzi Igora. Może być spowodowane przez: VAD (Gemini sam decyduje kiedy skończyłeś mówić), buforowanie audio w ws_server, lub opóźnienie sieci WiFi → PC.

## Do zbadania
- Czy Gemini Live API ma konfigurowalny VAD / end-of-speech sensitivity?
- Czy chunki docierają do Gemini bez opóźnień (logować timestamp)?
