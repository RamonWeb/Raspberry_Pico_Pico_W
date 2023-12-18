# Heizungssteuerung ohne WLAN
# by Perry Design (2023)
from machine import Pin, I2C
import utime
import dht
import ujson
from ssd1306 import SSD1306_I2C

# Konfiguration des I2C-Busses für das OLED-Display
i2c = I2C(1, sda=Pin(26), scl=Pin(27))
oled = SSD1306_I2C(128, 64, i2c)

# GPIO-Pins für DHT22-Sensoren
dht_internal = dht.DHT22(Pin(12))

# Konfiguration der Tasten-Pins
button1_pin = Pin(16, Pin.IN, Pin.PULL_DOWN)
button2_pin = Pin(17, Pin.IN, Pin.PULL_DOWN)
button3_pin = Pin(18, Pin.IN, Pin.PULL_DOWN)
stop_button_pin = Pin(19, Pin.IN, Pin.PULL_DOWN)

# GPIO-Pin für das Relais-Modul zur Steuerung der Heizung
# lt. Schaltung änderung auf pin8 und pin7
relay_pin1 = Pin(7, Pin.OUT)  # Heizung
fan_pin = Pin(8, Pin.OUT)  # Lüfter-Pin

# Voreingestellte Temperaturen für die Heizungssteuerung
preset_temperatures = [30.0, 40.0, 50.0]

# Variablen für die Programmsteuerung
target_temperature = None
program_running = False
selected_program = None
start_time = 0
# Initialisieren Sie die Variable
internal_temperature = 0.0
external_temperature = 99
program_names = target_temperature
humidity = 0
runtime = 0  # Initialisieren Sie die Variable für die Laufzeit
fan_running = False  # Variable, um den Lüfterstatus zu verfolgen
fan_shutdown_time = None  # Zeit, zu der der Lüfter abgeschaltet wird

relay_pin1.off() # Programmstart Heizung aus...
fan_pin.off()

def test_sensor_display():
    try:
        # Versuche, den Temperatursensor zu messen
        temperature, _ = messe_umgebung()
        
        # Versuche, das OLED-Display zu aktualisieren
        aktualisiere_oled_anzeige()
        
        # Wenn beide Versuche erfolgreich waren, zeige Erfolgsmeldung
        oled.fill(0)
        oled.text("Sensor & Display", 10, 10)
        oled.text("Test erfolgreich!", 10, 30)
        oled.show()
        
        utime.sleep(3)  # Warte 3 Sekunden, um die Meldung anzuzeigen

    except Exception as e:
        # Falls ein Fehler auftritt, zeige Fehlermeldung auf dem OLED-Display
        oled.fill(0)
        oled.text("Fehler beim Testen", 10, 10)
        oled.text("Error: {}".format(str(e)), 10, 30)
        oled.show()
        
        # Gib den Fehler auch in der Konsole aus
        print("Fehler beim Testen - Error:", e)

        utime.sleep(10)  # Warte 10 Sekunden, um die Fehlermeldung anzuzeigen
        raise  # Werfe die Ausnahme erneut, um den Fehler anzuzeigen


def control_fan(turn_on):
    global fan_running
    global fan_shutdown_time

    if turn_on:
        fan_pin.on()  # Lüfter einschalten
        fan_running = True
    else:
        if fan_running:
            fan_pin.off()  # Lüfter ausschalten
            fan_running = False
            fan_shutdown_time = utime.time() + 120  # Lüfter wird noch 2 Minuten nachlaufen

def control_heater(turn_on, target_temp):
    if turn_on:
        relay_pin1.on()  # Heizung einschalten
    else:
        # Wenn die Heizung ausgeschaltet werden soll und die Zieltemperatur erreicht ist, schalte sie aus
        if internal_temperature >= target_temp:
            relay_pin1.off()  # Heizung ausschalten
       
def messe_umgebung():
    dht_internal.measure()
    return dht_internal.temperature(), dht_internal.humidity()

def aktualisiere_oled_anzeige():
    oled.fill(0)
    oled.text("Temp: {:.1f}C".format(internal_temperature), 0, 0)
    oled.text("Humidity: {:.1f}%".format(humidity), 0, 16)
    oled.text("Set Temp: {}C".format(target_temperature), 0, 32)
    oled.text("Runtime: {}min".format(int((utime.time() - start_time) / 60)) if program_running else "Stopped", 0, 48)
    oled.show()
    
def main():
    display_logo()
    utime.sleep(5)
    logo_display_timer = utime.ticks_ms()

def display_logo():
    oled.fill(0)
    oled.text("Perry Design", 10, 20)
    oled.show()

def aktualisiere_zustand():
    # Hier aktualisieren Sie die Zustände, z.B. Temperatur, Feuchtigkeit, Laufzeit, usw.
    internal_temperature, humidity = messe_umgebung()
    # Weitere Aktualisierungen der Zustände hier...

def handle_button_press(target_temp, program_number):
    global target_temperature, selected_program, program_running, start_time

    target_temperature = target_temp
    selected_program = program_number
    program_running = True
    start_time = utime.time()

    if fan_running:
        control_fan(True)

# Rufe die Testfunktion auf
test_sensor_display()
utime.sleep(2)
# Initialisierung: Logo für 5 Sekunden anzeigen
display_logo()
utime.sleep(5)
logo_display_timer = utime.ticks_ms()  # Startzeit für das Logo setzen

while True:
    
    #internal_temp, luftfeuchtigkeit = messe_umgebung()
    internal_temperature, humidity = messe_umgebung()
    # Überwache Tastensteuerung 
    if button1_pin.value() == 1:
        handle_button_press(preset_temperatures[0], 1)
    elif button2_pin.value() == 1:
        handle_button_press(preset_temperatures[1], 2)
    elif button3_pin.value() == 1:
        handle_button_press(preset_temperatures[2], 3)
    elif stop_button_pin.value() == 1:
        if program_running:
            program_running = False
            start_time = 0
            target_temperature = 0
            control_fan(True)
            fan_shutdown_time = utime.time() + 60
            relay_pin1.off()
        else:
            control_fan(False)
            fan_shutdown_time = None
            relay_pin1.off()

    # Heizungssteuerung
    if program_running:
        if internal_temperature < target_temperature:
            control_heater(True, target_temperature)  # Heizung einschalten
            if not fan_running and not fan_pin.value():  # Wenn die Heizung neu eingeschaltet wird, schalte den Lüfter ebenfalls ein
                control_fan(True)
        else:
            control_heater(False, target_temperature)  # Heizung ausschalten, wenn Zieltemperatur erreicht

    # Überwachung des Lüfters nach Heizungsausschaltung oder Stoppen des Programms
    if fan_shutdown_time and utime.time() >= fan_shutdown_time:
        fan_shutdown_time = None  # Zurücksetzen der Shutdown-Zeit
        control_fan(False)  # Lüfter ausschalten

    # Aktualisieren Sie die OLED-Anzeige
    aktualisiere_oled_anzeige()
        
    # Überprüfen Sie, ob die Laufzeit von 6 Stunden erreicht wurde
    if program_running and (utime.time() - start_time) // 60 >= 6 * 60:  # 6 Stunden in Minuten
        program_running = False
        control_heater(False, target_temperature)  # Heizung ausschalten
        start_time = 0
        target_temperature = 0
        
    utime.sleep(1)