import time
import RPi.GPIO as GPIO
import numpy as np
import threading

def emit(period,duty,dur=3):
    """ send a signal with period and duty cycle """
    t1 = period*duty
    t2 = period - t1

    if not duty:
        GPIO.output(CH,0)
        time.sleep(dur)
        return

    for i in range(int(dur/period)):
        GPIO.output(CH,1)
        time.sleep(t1)
        GPIO.output(CH,0)
        time.sleep(t2)

CH = 20 
GPIO.setmode(GPIO.BCM)
GPIO.setup(CH,GPIO.OUT)
period = 0.005
duty = 0.5
dur = 1

for duty in [1,0.8,0.5,0.1,0.05,0.01,0]:
    print(f'duty = {duty*100}%')
    emit(period,duty,dur)

GPIO.cleanup()
