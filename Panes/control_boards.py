import sys
sys.path.append(".")
from Modules.tps_pmbus import TPS

try:
    tps10 = TPS("10")
    tps10.load_defaults()
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
    tps16 = TPS("16")
    tps16.load_defaults()
except IOError as e:
    pass

try:
    tps1d = TPS("1d")
    tps1d.load_defaults()
except IOError as e:
    pass
