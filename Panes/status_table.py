import sys
sys.path.append(".")
from Devices.tps_pmbus import TPS
from Devices.gpio_pins import PGOOD
from Devices.gpio_pins import TINTERLOCK
from Devices.gpio_pins import ALERT
from Devices.ds18b20 import ds18b20_write_queue
import tableprint as tp
import time
import os
import numpy as np
from multiprocessing import Process, Queue

# try to initilize boards with all kind of addresses
addresses = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1a", "1b", "1c", "1d", "1f"]
boards = []
for address in addresses:
    try:
        board = TPS(address)
        boards.append(board)
    except IOError as e:
        pass

# initialize gpio pins
pgood = PGOOD()
tinterlock = TINTERLOCK()
alert = ALERT()

# initialize temp sensor seperate process and queue
queue = Queue()
writer = Process(target=ds18b20_write_queue, args=((queue),))
writer.daemon = True
writer.start()
ds18b20_data = [("??",0), ("??",0)]  # dummy data to begin with
temp_address_trans = {"28-00000c443896": "TPS 1c", "28-00000a39aa04": "TPS 11", "28-00000a39366f": "TPS 10"}

i = 0
while True:
    i += 1
    os.system("clear")

    ### Table 1 ###
    width = 20

    header = [""]
    header.extend([f"TPS {format(board.device_address, '02x')}" for board in boards])
    print(tp.header(header, width=width))

    switch_freq = ["switch_freq"]
    switch_freq.extend([f"{board.get_switch_freq(verbose=False)} kHz" for board in boards])
    print(tp.row(switch_freq, width=width))

    on_off_bit = ["on_off_bit"]
    on_off_bit.extend([f"{board.get_on_off_bit(verbose=False)}" for board in boards])
    print(tp.row(on_off_bit, width=width))

    on_off_bit_behaviour = ["on_off_bit_behaviour"]
    on_off_bit_behaviour.extend([f"{board.get_on_off_bit_behaviour(verbose=False)}" for board in boards])
    print(tp.row(on_off_bit_behaviour, width=width))

    UVLO_threshold = ["UVLO_threshold"]
    UVLO_threshold.extend([f"{board.get_UVLO_threshold(verbose=False)} V" for board in boards])
    print(tp.row(UVLO_threshold, width=width))

    en_pin_behaviour = ["en_pin_behaviour"]
    en_pin_behaviour.extend([f"{board.get_en_pin_behaviour(verbose=False)}" for board in boards])
    print(tp.row(en_pin_behaviour, width=width))

    write_protection = ["write_protection"]
    write_protection.extend([f"{board.get_write_protection(verbose=False)}" for board in boards])
    print(tp.row(write_protection, width=width))

    # soft_start_config
    data = np.array([board.get_soft_start_config(verbose=False) for board in boards])
    soft_start_time = ["soft_start_time"]
    soft_start_time.extend(f"{i} ms" for i in data.T[0])
    print(tp.row(soft_start_time, width=width))
    hiccup = ["hiccup"]
    hiccup.extend(f"{i}" for i in data.T[1])
    print(tp.row(hiccup, width=width))
    fccm = ["fccm"]
    fccm.extend(f"{i}" for i in data.T[2])
    print(tp.row(fccm, width=width))

    print(tp.bottom(len(boards) + 1, width=width))

    ### Table 2 ###
    width = 10
    header = ["", "Slot 1", "Slot 2", "Slot 3", "Slot 4"]
    print(tp.header(header, width=width))

    powergood = ["PGOOD"]
    powergood.extend([int(i) for i in pgood.get_values()])
    print(tp.row(powergood, width=width))

    tempinterlock = ["TINTERLOCK"]
    tempinterlock.extend([int(i) for i in tinterlock.get_values()])
    print(tp.row(tempinterlock, width=width))

    alert_ = ["ALERT 1/2"]
    alert_.extend([int(i) for i in alert.get_values()])
    alert_.extend(["", ""])
    print(tp.row(alert_, width=width))

    print(tp.bottom(5, width=width))




    for board in boards:
        print("")
        print(f"TPS {format(board.device_address, '02x')}")
        print("------")
        board.get_status_word()

    print("")
    header = ["Address"]
    temps = ["Temp [°C]"]

    if not queue.empty():
        ds18b20_data = queue.get()

    for id, temp in ds18b20_data:
        if id in temp_address_trans:
            header.append(temp_address_trans[id])
        else:
            header.append(id)
        temps.append(f"{temp:.1f}")

    width = 20
    print(tp.header(header, width=width))
    print(tp.row(temps, width=width))
    print(tp.bottom(len(header), width=width))

    time.sleep(3)



# replace = ["replace"]
# replace.extend([f"{board.replace(verbose=False)} ??" for board in boards])
# print(tp.row(replace, width=width))
