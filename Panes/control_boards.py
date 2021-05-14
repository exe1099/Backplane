import sys
sys.path.append(".")
from Devices.tps_pmbus import TPS


# try to initilize boards with all kind of addresses
try:
    t10 = TPS("10")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("11")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("12")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("13")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("14")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("15")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("16")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("17")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("18")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("19")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("1a")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("1b")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("1c")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("1d")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("1e")
    t10.load_defaults()
except IOError as e:
    pass
try:
    t10 = TPS("1f")
    t10.load_defaults()
except IOError as e:
    pass