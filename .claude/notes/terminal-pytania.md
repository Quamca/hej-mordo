# Pytania/komunikaty do wyciszenia

Wklej tu pytania lub komunikaty z terminala których nie chcesz widzieć.
Claude sprawdzi po każdej sesji co da się wyciszyć.

## Do sprawdzenia

 Bash command
   powershell -Command "Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*monitor*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
   Zamknij Serial Monitor

 Contains simple_expansion

 Do you want to proceed?
 ❯ 1. Yes
   2. No

 Bash command
   cd "C:/Users/Maluszek/Desktop/kosz/AI/Hej Mordo/firmware" && "$USERPROFILE/.platformio/penv/Scripts/pio.exe" run -e test_display --target upload 2>&1
   Upload test_display firmware na ESP32-S3

 Contains simple_expansion

 Do you want to proceed?
 ❯ 1. Yes
   2. No

## Już wyciszone

- `Edit(**)` — edycja plików (display.cpp i inne) bez pytania
- `Bash(powershell*)` — kill Serial Monitor bez ostrzeżenia "Contains simple_expansion"
- `Bash(*pio.exe*)` — PlatformIO upload bez ostrzeżenia "Contains simple_expansion"
- `Bash(cd * && git *)` — git commit z cd bez ostrzeżenia (reguła była już, teraz też Edit i powershell dodane)
