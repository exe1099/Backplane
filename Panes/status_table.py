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


# buffered print
buffered_output = ""
def bprint(str: s, bool: reset = False):
    if reset:
        os.system("clear")
        print(buffered_output)
        buffered_output = ""
    else:
        buffered_output = buffered_output + s + "\n"

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
ds18b20_data = [("??", 0), ("??", 0)]  # dummy data to begin with
temp_address_trans = {
    "28-00000c443896": "TPS 1c",
    "28-00000a39aa04": "TPS 11",
    "28-00000a39366f": "TPS 10",
}

os.system("clear")
while True:

    ### Main Table (Board specific) ###
    width = 20

    # header
    header = [""]
    header.extend([f"TPS {format(board.device_address, '02x')}" for board in boards])
    bprint(tp.header(header, width=width))

    # switching frequency
    switch_freq = ["switch_freq"]
    switch_freq.extend(
        [f"{board.get_switch_freq(verbose=False)} kHz" for board in boards]
    )
    bprint(tp.row(switch_freq, width=width))

    # on-off bit
    on_off_bit = ["on_off_bit"]
    on_off_bit.extend([f"{board.get_on_off_bit(verbose=False)}" for board in boards])
    bprint(tp.row(on_off_bit, width=width))

    # on-off bit behaviour
    on_off_bit_behaviour = ["on_off_bit_behaviour"]
    on_off_bit_behaviour.extend(
        [f"{board.get_on_off_bit_behaviour(verbose=False)}" for board in boards]
    )
    bprint(tp.row(on_off_bit_behaviour, width=width))

    # UVLO threshold
    UVLO_threshold = ["UVLO_threshold"]
    UVLO_threshold.extend(
        [f"{board.get_UVLO_threshold(verbose=False)} V" for board in boards]
    )
    bprint(tp.row(UVLO_threshold, width=width))

    # en-pin behaviour
    en_pin_behaviour = ["en_pin_behaviour"]
    en_pin_behaviour.extend(
        [f"{board.get_en_pin_behaviour(verbose=False)}" for board in boards]
    )
    bprint(tp.row(en_pin_behaviour, width=width))

    # write protection
    write_protection = ["write_protection"]
    write_protection.extend(
        [f"{board.get_write_protection(verbose=False)}" for board in boards]
    )
    bprint(tp.row(write_protection, width=width))

    # soft_start_config
    data = np.array([board.get_soft_start_config(verbose=False) for board in boards])
    soft_start_time = ["soft_start_time"]
    soft_start_time.extend(f"{i} ms" for i in data.T[0])
    bprint(tp.row(soft_start_time, width=width))
    hiccup = ["hiccup"]
    hiccup.extend(f"{i}" for i in data.T[1])
    bprint(tp.row(hiccup, width=width))
    fccm = ["fccm"]
    fccm.extend(f"{i}" for i in data.T[2])
    bprint(tp.row(fccm, width=width))

    # bottom
    bprint(tp.bottom(len(boards) + 1, width=width))

    ### Second Table (Slot specific) ###
    width = 10

    # header
    header = ["", "Slot 1", "Slot 2", "Slot 3", "Slot 4"]
    bprint(tp.header(header, width=width))

    # powergood
    powergood = ["PGOOD"]
    powergood.extend([int(i) for i in pgood.get_values()])
    bprint(tp.row(powergood, width=width))

    # temp interlock
    tempinterlock = ["TINTERLOCK"]
    tempinterlock.extend([int(i) for i in tinterlock.get_values()])
    bprint(tp.row(tempinterlock, width=width))

    # alert
    alert_ = ["ALERT 1/2"]
    alert_.extend([int(i) for i in alert.get_values()])
    alert_.extend(["", ""])
    bprint(tp.row(alert_, width=width))

    # enable switch state
    # read state from file (there must be a better way to transfer data...)
    try:
        with open("enable_switch_state.txt", "r") as file:
            state = file.read().split(" ")
    except FileNotFoundError:
        state = ["?", "?", "?", "?"]

    en_switch = ["ENABLE SWITCH"]
    en_switch.extend(s for s in state)
    bprint(tp.row(en_switch, width=width))

    # bottom
    bprint(tp.bottom(5, width=width))

    ### Status Words ###
    for board in boards:
        bprint("")
        bprint(f"TPS {format(board.device_address, '02x')}")
        bprint("------")
        board.get_status_word()
    bprint("")

    ### Temp Table ###
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
    bprint(tp.header(header, width=width))
    bprint(tp.row(temps, width=width))
    bprint(tp.bottom(len(header), width=width))

    ### Print buffered Output ###
    bprint("", reset=True)

    ### Refresh Wait ###
    time.sleep(3)