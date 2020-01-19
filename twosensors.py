import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import board
import RPi.GPIO as GPIO
import adafruit_dht
import datetime
import os
import threading

from ledThread import LED

def main():
    """ Setu-up SPI for MAX6675, GPIOs for DHT11 and LEDs
    and run the main loop with data aquisition, saving 
    data to a csv file.
    """
    global leds

    CHS = [21,20,16]
    setup_LEDs(CHS)
    pi = pigpio.pi()

    if not pi.connected:
       exit(0)

    sensor = pi.spi_open(0, 1000000, 0)   # CE0, 1Mbps, main SPI

    stop = time.time() + 6000

    dhtDevice = adafruit_dht.DHT11(board.D12)

    datafolder = '../data'

    fname = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.txt'

    fname = os.path.join(datafolder,fname)
    with open(fname,'a') as f:
        f.write('time, DHT11 T[C],DHT11 H[%],MAX667 T[C]\n')

    while True: #time.time() < stop:
        c, d = pi.spi_read(sensor, 2)
        if c == 2:
            word = (d[0]<<8) | d[1]
            if (word & 0x8006) == 0: # Bits 15, 2, and 1 should be zero.
                t = (word >> 3)/4.0
                t = f'{t:.1f}'
                #print(f"{t:.2f}")
            else:
                print("bad reading {word:b}")

        # Don't try to read more often than 4 times a second.
        #time.sleep(0.25) 
        temperature_c = 'nan'
        humidity = 'nan'
        try:
            # Print the values to the serial port
            temperature_c = f'{dhtDevice.temperature:.1f}'
            #temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            
            """ Control indicator LEDs here """
            updateLEDs(humidity,[30,55])

            humidity = f'{humidity}'
        except RuntimeError as error:
            pass
            #print(error.args[0])
                
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        if int(now[-5:-3])%30 == 0:
            leds['blue'].on()
            leds['blue'].blink_start()
        else:
            leds['blue'].off()
            leds['blue'].blink_stop()

        print(f"{now} T: {temperature_c}C H: {humidity}% K: {t}C")
        
        with open(fname,'a') as f:
            f.write(f"{now}, {temperature_c}, {humidity}, {t}\n")

        time.sleep(2)

    pi.spi_close(sensor)
    pi.stop()
    GPIO.cleanup()

def updateLEDs(humidity,lims = [30,50]):
    """ Control indicator LEDs here """
    #print(humidity,lims[1],lims[0])
    global leds

    if humidity > lims[1]:
        change_leds('red')
    elif humidity<lims[0]:
        change_leds('blue')
    else:
        change_leds('green')

def change_leds(name):
    """ """
    global leds
    
    for n,led in leds.items():
        if n == name:
            led.on()
        else:
            led.off()

def setup_LEDs(CHS = [21,20,16]):
    """ Setup GPIOs for LEDs """
    global leds

    GPIO.setmode(GPIO.BCM)

    for CH in CHS:
        GPIO.setup(CH, GPIO.OUT)

    period = 0.008
    duties = [0.08,0.01,0.08]
    dur = 0.3
    # define leds
    nms = ['red','green','blue']
    leds  = {n:LED(CH,duty,period) for CH,duty,n in zip(CHS,duties,nms)}
    [led.blink_setup(durs=[1,1]) for led in leds.values()]
    [led.start() for led in leds.values()]
    [led.off() for led in leds.values()]

def stop_LEDs(CHS):
    """ Turn LEDs off, such as before quiting """
    global leds

    [led.off() for led in leds.values()]

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        [led.stop() for led in leds.values()]
        [led.join() for led in leds.values()]
        GPIO.cleanup()
        print('\nGPIO cleaned up after interruption')
