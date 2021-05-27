import glob
import time
from multiprocessing import Process, Queue

# activate 1-wire interface with: sudo dtoverlay w1-gpio gpiopin=14 pullup=0

while True:

   for sensor in glob.glob("/sys/bus/w1/devices/28-00*/w1_slave"):
      id = sensor.split("/")[5]

      try:
         f = open(sensor, "r")
         data = f.read()
         f.close()
         if "YES" in data:
            (discard, sep, reading) = data.partition(' t=')
            t = float(reading) / 1000.0
            print("{} {:.1f}".format(id, t))
         else:
            print("999.9")

      except:
         pass

   time.sleep(3.0)