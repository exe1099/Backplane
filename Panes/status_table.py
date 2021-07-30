import sys

sys.path.append(".")
from Devices.tps_pmbus import TPS
from Devices.gpio_pins import PGOOD
from Devices.gpio_pins import TINTERLOCK
from Devices.gpio_pins import ALERT
from Devices.ds18b20 import ds18b20_write_queue
from Panes.t_colors import TColors
import tableprint as tp
import time
import os
import numpy as np
from multiprocessing import Process, Queue


# try to initilize boards with all kind of addresses
addresses = [
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "1a",
    "1b",
    "1c",
    "1d",
    "1f",
]
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
ds18b20_data = [("??", 0, "??"), ("??", 0, "??")]  # dummy data to begin with

os.system("clear")
while True:

    ### Main Table (Board specific) ###
    width = 20

    # header
    header = [""]
    header.extend([f"TPS {format(board.device_address, '02x')}" for board in boards])
    print(tp.header(header, width=width))

    # on-off bit
    on_off_bit = ["on_off_bit"]
    for board in boards:
        i = board.get_on_off_bit(verbose=False)
        if int(i):
            on_off_bit.append(TColors.GREEN + i + TColors.END)
        else:
            on_off_bit.append(TColors.RED + i + TColors.END)
    # on_off_bit.extend([f"{board.get_on_off_bit(verbose=False)}" for board in boards])
    print(tp.row(on_off_bit, width=width))

    # on-off bit behaviour
    on_off_bit_behaviour = ["on_off_bit_behaviour"]
    on_off_bit_behaviour.extend(
        [f"{TColors.BLUE + board.get_on_off_bit_behaviour(verbose=False) + TColors.END}" for board in boards]
    )
    print(tp.row(on_off_bit_behaviour, width=width))

    # en-pin behaviour
    en_pin_behaviour = ["en_pin_behaviour"]
    en_pin_behaviour.extend(
        [f"{TColors.BLUE + board.get_en_pin_behaviour(verbose=False) + TColors.END}" for board in boards]
    )
    print(tp.row(en_pin_behaviour, width=width))

    # switching frequency
    switch_freq = ["switch_freq"]
    switch_freq.extend(
        [f"{board.get_switching_freq(verbose=False)} kHz" for board in boards]
    )
    print(tp.row(switch_freq, width=width))

    # UVLO threshold
    UVLO_threshold = ["UVLO_threshold"]
    UVLO_threshold.extend(
        [f"{board.get_UVLO_threshold(verbose=False)} V" for board in boards]
    )
    print(tp.row(UVLO_threshold, width=width))

    # write protection
    write_protection = ["write_protection"]
    write_protection.extend(
        [f"{board.get_write_protection(verbose=False)}" for board in boards]
    )
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

    # bottom
    print(tp.bottom(len(boards) + 1, width=width))

    ### Second Table (Slot specific) ###
    width = 15

    # header
    header = ["", "Slot 1", "Slot 2", "Slot 3", "Slot 4"]
    print(tp.header(header, width=width))

    # powergood
    powergood = ["PGOOD"]
    for i in pgood.get_values():
        if i:
            powergood.append(TColors.GREEN + str(int(i)) + TColors.END)
        else:
            powergood.append(str(int(i)))
    # powergood.extend([int(i) for i in pgood.get_values()])
    print(tp.row(powergood, width=width))

    # temp interlock
    tempinterlock = ["TINTERLOCK"]
    for i in tinterlock.get_values():
        if i:
            tempinterlock.append(TColors.RED + str(int(i)) + TColors.END)
        else:
            tempinterlock.append(str(int(i)))
    print(tp.row(tempinterlock, width=width))

    # enable switch state
    # read state from file (there must be a better way to transfer data...)
    try:
        with open("enable_switch_state.txt", "r") as file:
            state = file.read().split(" ")
    except FileNotFoundError:
        state = ["?", "?", "?", "?"]

    en_switch = ["ENABLE SWITCH"]
    for s in state:
        if int(s):
            en_switch.append(TColors.GREEN + s + TColors.END)
        else:
            en_switch.append(TColors.RED + s + TColors.END)
    print(tp.row(en_switch, width=width))

    # alert
    alert_ = ["ALERT 1/2"]
    alert_.extend([int(i) for i in alert.get_values()])
    alert_.extend(["", ""])
    print(tp.row(alert_, width=width))

    # bottom
    print(tp.bottom(5, width=width))

    ### Status Words ###
    for board in boards:
        print("")
        print(f"TPS {format(board.device_address, '02x')}")
        print("------")
        board.get_status_word()
    print("")

    ### Temperature Table ###
    header = ["Address"]
    temps = ["Temp [°C]"]
    time_ = ["Time"]

    if not queue.empty():
        ds18b20_data = queue.get()

    for board, temp, measurement_time in ds18b20_data:
        header.append(board)
        temps.append(f"{temp:.1f}")
        time_.append(measurement_time)

    width = 20
    try:
        print(tp.header(header, width=width))
        print(tp.row(temps, width=width))
        print(tp.row(time_, width=width))
        print(tp.bottom(len(header), width=width))
    except TypeError:
        pass

    ### Refresh Wait ###
    time.sleep(3)
    os.system("clear")
