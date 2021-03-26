from Modules.tps_pmbus import TPS

try:
    tps15 = TPS("15")
    tps15.load_defaults()

    tps16 = TPS("16")
    tps16.load_defaults()

    tps15 = TPS("1a")
    tps15.load_defaults()

    tps15 = TPS("1b")
    tps15.load_defaults()

    tps15 = TPS("1c")
    tps15.load_defaults()

    tps15 = TPS("16")
    tps15.load_defaults()

except IOError as e:
    pass
