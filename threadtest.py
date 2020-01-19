import threading
import time

class LED(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super().__init__()
        self.__stop = False

    def run(self):
        """ """
        print('inside')
        i = 0

        while i < 10 and not self.__stop:
            time.sleep(0.5)
            print(i)
            i+=1

        print('finishing')

    def stop(self):
        """ """
        self.__stop = True

try:
    t1 = LED() 
    t1.start() 
    print('meanwhile')
    time.sleep(2)
    print('next main step')
    t1.join() 
except KeyboardInterrupt:
    print('\nWill close thread after current event processed')
    t1.stop()
