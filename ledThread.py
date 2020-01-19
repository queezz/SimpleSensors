import time
import RPi.GPIO as GPIO
import numpy as np
import threading

class LED(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,pin,duty,period=0.005):
        super().__init__()
        self.__stop = False
        self.__off = False
        self.__pin = pin
        self.setup(duty,period)
        self.blink_setup()

    def blink_setup(self,durs = [0.05,0.05]):
        """ setup LED blinking times and state. durs = [time on, time off] """
        self.blink_on= False # blink = True, do not blink = False 
        self.blink_state = 1 # LED ON = 1, LED OFF = 0
        self.blink_durs = durs
        self.blink_t = self.blink_durs[0]

    def blink_changestate(self):
        """ change blink state between ON and OFF"""
        if self.blink_state:
            self.blink_t = self.blink_durs[1]
            self.blink_state = 0
            self.blink_timer = time.time()
        else:
            self.blink_t = self.blink_durs[0]
            self.blink_state = 1
            self.blink_timer = time.time()

    def blink_start(self):
        """ start to blink """
        self.blink_on = True
        self.blink_state = 1
        self.blink_timer = time.time()

    def blink_stop(self):
        """ start to blink """
        self.blink_state = 1 # used in PWD condition, must be 1
        self.blink_on = False 

    def stop(self):
        """ Turn OFF LED and stop main loop """
        CH = self.__pin
        self.__stop = True

    def setup(self,duty,period=0.005):
        """ Setup Pulse parameters """
        #print(f'duty = {duty*100:.0f}%')
        self.duty = duty
        if duty == 0:
            self.off()
        else:
            self.on()

        self.period = period
        self.t1 = period*duty
        self.t2 = period - self.t1

    def off(self):
        """ Turn LED OFF, but keep the thread alive """
        self.__off = True

    def on(self):
        """ Turn LED ON """
        self.__off = False 

    def run(self):
        """ start loop with given duty until interrupted """
        CH = self.__pin

        while not self.__stop:
            # if self.duty == 0, don't send voltage to LED
            if self.blink_on:
                if time.time()-self.blink_timer > self.blink_t:
                    self.blink_changestate()

            if not self.__off and self.blink_state:
                GPIO.output(CH,1)
                time.sleep(self.t1)
            else:
                GPIO.output(CH,0)

            GPIO.output(CH,0)
            time.sleep(self.t2)

def test_one_led():
    """ test one led"""
    CH = 20 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CH,GPIO.OUT)
    period = 0.005
    duty = 0.1
    dur = 3

    led = LED(CH,duty,period)
    led.start()

    print('led ON')
    time.sleep(dur)
    print('attempt to turn of LED')
    led.stop()
    led.join()

    GPIO.cleanup()

def test_several():
    CHS = [20,21,16]
    GPIO.setmode(GPIO.BCM)
    [GPIO.setup(CH,GPIO.OUT) for CH in CHS]
    period = 0.005
    duties = [0.1,0.5,0.5]
    dur = 3
    nms = ['red','green','blue']
    leds  = {n:LED(CH,duty,period) for CH,duty,n in zip(CHS,duties,nms)}
    [led.start() for led in leds.values()]

    time.sleep(dur)
    [led.stop() for led in leds.values()]

    GPIO.cleanup()

def test_change_duty():
    CHS = [20,21,16]
    GPIO.setmode(GPIO.BCM)
    [GPIO.setup(CH,GPIO.OUT) for CH in CHS]
    period = 0.005
    duties = np.ones(3) 
    dur = 0.3
    # define leds
    nms = ['red','green','blue']
    leds  = {n:LED(CH,duty,period) for CH,duty,n in zip(CHS,duties,nms)}

    # start led threads
    [led.start() for led in leds.values()]
    print('started')
    time.sleep(dur)

    print('turn off')
    [led.off() for led in leds.values()]
    time.sleep(dur)

    print('50%')
    duties = np.ones(3)*0.5
    [led.setup(duty=d) for led,d in zip(leds.values(),duties)]
    time.sleep(dur)

    print('10%')
    duties = np.ones(3)*0.1
    [led.setup(duty=d) for led,d in zip(leds.values(),duties)]
    time.sleep(dur)
    print('finish')

    [led.stop() for led in leds.values()]
    # wait for all threads to finish
    [led.join() for led in leds.values()]
    GPIO.cleanup()

def test_blink():
    """ blink one LED """
    CHS = [21,20,16]
    GPIO.setmode(GPIO.BCM)
    [GPIO.setup(CH,GPIO.OUT) for CH in CHS]
    period = 0.005
    duties = [0.3,0.05,0.3]
    dur = 1
    nms = ['red','green','blue']
    leds  = {n:LED(CH,duty,period) for CH,duty,n in zip(CHS,duties,nms)}
    
    [led.blink_setup(durs=[0.02,0.08]) for led in leds.values()]
    [led.blink_start() for led in leds.values()]
    [led.start() for led in leds.values()]

    time.sleep(dur)
    [led.blink_stop() for led in leds.values()]
    time.sleep(dur)
    
    [led.blink_start() for led in leds.values()]
    time.sleep(dur)
    
    [led.stop() for led in leds.values()]
    # wait for all threads to finish
    [led.join() for led in leds.values()]
    GPIO.cleanup()

if __name__ == "__main__":
    ""
    #test_one_led()
    #test_several()
    #test_change_duty()
    test_blink()
