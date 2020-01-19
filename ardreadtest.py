from nanpy import (ArduinoApi, SerialManager)
from time import sleep

pot = 14

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except Error as err:
    print(f"Failed to connect to Arduino {err}")

# Setup the pinModes as if we were in the Arduino IDE
#a.pinMode(ledPin, a.OUTPUT)
#a.pinMode(buttonPin,a.INPUT)

try:
    while True:
        val = a.analogRead(pot)
        print(f'{val/1023*5:.2f} {val}')
        sleep(0.1)

except Exception as err:
    print(f'{err}')
