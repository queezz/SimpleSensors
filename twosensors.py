import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import board
import RPi.GPIO as GPIO
import adafruit_dht
import datetime

def main():
    """ Setu-up SPI for MAX6675, GPIOs for DHT11 and LEDs
    and run the main loop with data aquisition, saving 
    data to a csv file.
    """
    clrs = {'red':0,'green':1,'blue':2}
    CHS = [21,20,16]
    setup_LEDs(CHS)
    pi = pigpio.pi()

    if not pi.connected:
       exit(0)

    sensor = pi.spi_open(0, 1000000, 0)   # CE0, 1Mbps, main SPI

    stop = time.time() + 6000

    dhtDevice = adafruit_dht.DHT11(board.D12)

    fname = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.txt'
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
            updateLEDs(humidity,clrs,[30,55],CHS)
            humidity = f'{humidity}'
        except RuntimeError as error:
            pass
            #print(error.args[0])
                
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(f"{now} T: {temperature_c}C H: {humidity}% K: {t}C")
        
        with open(fname,'a') as f:
            f.write(f"{now}, {temperature_c}, {humidity}, {t}\n")

        time.sleep(2)

    pi.spi_close(sensor)
    pi.stop()
    GPIO.cleanup()

def updateLEDs(humidity,clrs,lims = [30,50],CHS = [21,20,16]):
    """ Control indicator LEDs here """
    #clrs = {'red':0,'green':1,'blue':2}
    #print(humidity,lims[1],lims[0])

    if humidity > lims[1]:
        led_indicator(clrs['red'],CHS)
    elif humidity<lims[0]:
        led_indicator(clrs['blue'],CHS)
    else:
        led_indicator(clrs['green'],CHS)

def setup_LEDs(CHS = [21,20,16]):
    """ Setup GPIOs for LEDs """
    GPIO.setmode(GPIO.BCM)

    for CH in CHS:
        GPIO.setup(CH, GPIO.OUT)

def stop_LEDs(CHS):
    """ Turn LEDs off, such as before quiting """
    [GPIO.output(CH,0) for CH in CHS]

def led_indicator(led_ind=0, CHS=[21,20,16]):
    """ Indicate the humidity level with 3 LEDs:
    HIGH - RED, OPTIMAL - GREEN, LOW - BLUE
    """
    
    for i,CH in enumerate(CHS):
       if i == led_ind:
           GPIO.output(CH,1)
       else:
           GPIO.output(CH,0) 

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('\nGPIO cleaned up after interruption')
