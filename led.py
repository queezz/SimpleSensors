import time
import RPi.GPIO as GPIO
import numpy as np


def prog1(CHS = [21,20,16]):
    """ LED test """
    setup_pins(CHS)

    for dt in [0.3,0.1,0.05,0.01]:
        for i in range(9):
            set_led(i%3,CHS)
            time.sleep(dt)

    R = range(100)
    t = np.linspace(0,np.pi,len(R))
    times = 0.1*np.sin(t)**2

    for i,j in enumerate(R):
        time.sleep(times[i])

        for CH in CHS:
            GPIO.output(CH,i%2)

    turn_off(CHS)

def set_led(led_ind = 0,CHS=[21,20,16]):
    """ Set one LED ON while turning others OFF """
    
    for i,CH in enumerate(CHS):
       if i == led_ind:
           GPIO.output(CH,1)
       else:
           GPIO.output(CH,0) 

def turn_off(CHS):
    """ Turn off all LEDs """
    [GPIO.output(CH,0) for CH in CHS]
    GPIO.cleanup()
    print('\nGPIO cleaned up after interruption')

def setup_pins(CHS = [21,20,16]):
    """ setup GPIO pins to write mode"""
    GPIO.setmode(GPIO.BCM)
    [GPIO.setup(CH, GPIO.OUT) for CH in CHS]
    
def dim(CHS = [21,20,16]):
    """ Blink using GPIO PWM """
    setup_pins(CHS)
    nms = ['led1','led2','led3']
    leds = {n:GPIO.PWM(CH,50) for n,CH in zip(nms,CHS)}
    [led.start(0) for led in leds.values()] 

    while True:
        for i in range(100):
            [led.ChangeDutyCycle(i) for led in leds.values()] 
            time.sleep(0.02)
        for i in range(100):
            [led.ChangeDutyCycle(100-i) for led in leds.values()] 
            time.sleep(0.02)

    #[led.stop() for led in leds.values()] 

if __name__ == "__main__":
    try:
        #prog1()
        dim()
    except KeyboardInterrupt:
        turn_off(CHS = [21,20,16])
