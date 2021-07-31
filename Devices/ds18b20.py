import glob
import time
# from multiprocessing import Process, Queue

# activate 1-wire interface with: sudo dtoverlay w1-gpio gpiopin=14 pullup=0


def read_sensors():
    temp_address_trans = {
        "28-00000c443896": "TPS_1c",
        "28-00000a394789": "TPS_1b",
        "28-00000a39aa04": "TPS_11",
        "28-00000a39366f": "TPS_10",
        "28-00000a3a49a2": "Ambient",
    }

    data_sensors = []

    for sensor in glob.glob("/sys/bus/w1/devices/28-00*/w1_slave"):
        id = sensor.split("/")[5]

        try:
            with open(sensor, "r") as f:
                data = f.read()
            if "YES" in data:
                (discard, sep, reading) = data.partition(' t=')
                temp = float(reading) / 1000.0
                current_time = time.localtime()
                current_time = time.strftime("%H:%M:%S", current_time)
                board_id = temp_address_trans[id] if id in temp_address_trans else id
                # save board_id, temperature, current time (to check if data is up-to-date)
                data_sensors.append((board_id, temp, current_time))
            else:
                # in case sensor is not rdy or so
                data_sensors.append((-1, -1, -1))
        except:
            pass

        return data_sensors


def log_data_func(data_sensors):
    with open("Data/temperatures.data", "a") as file:
        for entry in data_sensors:
            # write for each sensor one line
            entry = [str(x) for x in entry]
            file.write("\t".join(entry) + "\n")


def run_queue(queue, log_data = True, refresh_time = 2):

    while True:

        data_sensors = read_sensors()
        # readout queue until empty, since we only want the most current values in there
        while not queue.empty():
            queue.get()
        queue.put(data_sensors)

        if log_data:
            log_data_func(data_sensors)

        time.sleep(refresh_time)

if __name__ == "__main__":
    print("Here one can write some more code.")
