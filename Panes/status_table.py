import sys
sys.path.append(".")
from Devices.tps_pmbus import TPS
import tableprint as tp
import time
import os
import numpy as np

# try to initilize boards with all kind of addresses
addresses = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1a", "1b", "1c", "1d", "1f"]
boards = []
for address in addresses:
    try:
        board = TPS(address)
        boards.append(board)
    except IOError as e:
        pass
print(boards)

i = 0

while True:
    i += 1
    os.system("clear")

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

    for board in boards:
        print("")
        print(f"TPS {format(board.device_address, '02x')}")
        print("------")
        board.get_status_word()

    print("")
    print("")
    print(f"Update-Counter: {i}")

    time.sleep(3)



# replace = ["replace"]
# replace.extend([f"{board.replace(verbose=False)} ??" for board in boards])
# print(tp.row(replace, width=width))