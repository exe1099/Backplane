import glob
import time
# from multiprocessing import Process, Queue

# activate 1-wire interface with: sudo dtoverlay w1-gpio gpiopin=14 pullup=0

def ds18b20_write_queue(queue, use_queue = True):

    log_data = False

    while True:

        values = []

        for sensor in glob.glob("/sys/bus/w1/devices/28-00*/w1_slave"):
            id = sensor.split("/")[5]

            try:
                f = open(sensor, "r")
                data = f.read()
                f.close()
                if "YES" in data:
                    (discard, sep, reading) = data.partition(' t=')
                    t = float(reading) / 1000.0
                    current_time = time.localtime()
                    current_time = time.strftime("%H:%M:%S", current_time)
                    values.append((id, t, current_time))
                else:
                    values.append((-1, -1, -1))

            except:
                pass
        if use_queue:
            if queue.empty():
                queue.put(values)
        else:
            print(values)

        if log_data:
            with open("temperatures.data", "a") as file:
                for device in values:
                    id_, temp_, time_ = device
                    file.write(f"{id_} {temp_} {time_}\n")

        time.sleep(1)

if __name__ == "__main__":
    abc = []
    ds18b20_write_queue(abc, use_queue = False)
