import time
import RPi.GPIO as GPIO
import numpy as np

def main(CHS = [21,20,16]):
    """ LED test """
    GPIO.setmode(GPIO.BCM)

    for CH in CHS:
        GPIO.setup(CH, GPIO.OUT)
        GPIO.output(CH,1) 

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
    GPIO.cleanup()

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
    
if __name__ == "__main__":
    try:
        for i in range(100):
            main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('\nGPIO cleaned up after interruption')
