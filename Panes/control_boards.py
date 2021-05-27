import sys
sys.path.append(".")
from Devices.tps_pmbus import TPS
from Devices.gpio_pins import ENABLE_SWITCH
import os

os.system("clear")

switch = ENABLE_SWITCH()
print("Controll of enable-switch: switch.set(<n_slot>, <0 or 1>)")


# try to initilize boards with all kind of addresses
try:
    tps10 = TPS("10")
    tps10.load_defaults()
except IOError as e:
    pass
try:
    tps11 = TPS("11")
    tps11.load_defaults()
except IOError as e:
    pass
try:
    tps12 = TPS("12")
    tps12.load_defaults()
except IOError as e:
    pass
try:
    tps13 = TPS("13")
    tps13.load_defaults()
except IOError as e:
    pass
try:
    tps14 = TPS("14")
    tps14.load_defaults()
except IOError as e:
    pass
try:
    tps15 = TPS("15")
    tps15.load_defaults()
except IOError as e:
    pass
try:
    tps16 = TPS("16")
    tps16.load_defaults()
except IOError as e:
    pass
try:
    tps17 = TPS("17")
    tps17.load_defaults()
except IOError as e:
    pass
try:
    tps18 = TPS("18")
    tps18.load_defaults()
except IOError as e:
    pass
try:
    tps19 = TPS("19")
    tps19.load_defaults()
except IOError as e:
    pass
try:
    tps1a = TPS("1a")
    tps1a.load_defaults()
except IOError as e:
    pass
try:
    tps1b = TPS("1b")
    tps1b.load_defaults()
except IOError as e:
    pass
try:
    tps1c = TPS("1c")
    tps1c.load_defaults()
except IOError as e:
    pass
try:
    tps1d = TPS("1d")
    tps1d.load_defaults()
except IOError as e:
    pass
try:
    tps1e = TPS("1e")
    tps1e.load_defaults()
except IOError as e:
    pass
try:
    tps1f = TPS("1f")
    tps1f.load_defaults()
except IOError as e:
    pass