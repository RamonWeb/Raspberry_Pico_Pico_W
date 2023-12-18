# Raspberry Pico (Pico W)

Heizungsteuerung für einen Filament Trockner und Aufbewahrung
sowie Bauraum Heizung für meine 3D Drucker

Heating control for a filament dryer and storage
as well as build space heating for my 3D printers

  1.MICRO PYTHON CODE --> main.py
  
  2.Pico-Steuerung auf Steckplatine (Testaufbau) --> pico_steuerung_Steckplatine.jpg (*.pdf)
  

# Heizungssteuerung ohne WLAN

Dieses Projekt wurde von Perry Design im Jahr 2023 entwickelt. Es handelt sich um eine Heizungssteuerung ohne WLAN, die auf einem Mikrocontroller läuft und Sensoren zur Temperatur- und Luftfeuchtigkeitsmessung verwendet.

## Funktionen

- Steuerung der Heizung basierend auf voreingestellten Temperaturen
- Überwachung der internen Temperatur und Luftfeuchtigkeit mit einem DHT22-Sensor
- Anzeige von Informationen auf einem OLED-Display
- Einfache Bedienung über Tasten

## Hardware-Konfiguration

- OLED-Display über I2C
- DHT22-Sensor für die interne Temperatur und Luftfeuchtigkeit
- Tasten für die Bedienung
- Relais-Modul zur Steuerung der Heizung
- Lüfter zur Belüftung

## Installation und Verwendung

1. Klone das Repository.
2. Passe die Konfiguration an, wenn notwendig.
3. Lade den Code auf deinen Mikrocontroller hoch.
4. Verbinde die Hardware entsprechend der Dokumentation.

## Fehlerbehebung

### Sensor- und Display-Test

Wenn du das Programm startest, wird automatisch ein Test für den Temperatursensor und das OLED-Display durchgeführt. Bei Problemen wird eine Fehlermeldung auf dem Display angezeigt.

## Autoren

- Perry Design (GitHub: [RamonWeb](https://github.com/RamonWeb))

## Unterstützung

Wenn dir dieses Projekt gefällt, kannst du mich gerne unterstützen. Kaffee geht immer! ☕

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-yellow.svg)](https://www.buymeacoffee.com/perrydesign)

## Weitere Informationen

Besuche auch meinen YouTube-Kanal für weitere Projekte und Tutorials: [Perry Design YouTube](https://youtube.com/@perry-design)
