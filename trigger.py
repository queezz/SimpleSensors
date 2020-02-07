import time
import RPi.GPIO as GPIO
import numpy as np


def setup_pins(CHS = [21,20,16]):
    """ setup GPIO pins to write mode"""
    GPIO.setmode(GPIO.BCM)
    [GPIO.setup(CH, GPIO.OUT) for CH in CHS]

def turn_off(CHS):
    """ Turn off all LEDs """
    [GPIO.output(CH,0) for CH in CHS]
    GPIO.cleanup()
    print('\nGPIO cleaned up after interruption')

def main(CH=26):
    ""
    setup_pins(CHS = [CH])

    while True:
        pattern = [0.5,0.5,0.5,2]
        [signl(CH,not i%2, dt) for i,dt in enumerate(pattern)]

def signl(CH,v,dt):
    ""
    GPIO.output(CH,v)
    time.sleep(dt)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        turn_off(CHS = [26])
