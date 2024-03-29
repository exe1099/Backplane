import time
import Adafruit_ADS1x15
import tableprint as tp
import numpy as np


class ADC:

    gain_limits = {1: 4.096, 2: 2.048, 4: 1.024, 8: 0.512, 16: 0.256}
    max_bin = 2 ** 16 - 1

    def __init__(self, device_address: str = "48", name: str = "???", bus: int = 4, gain: int = 1, unit: int = 1, current_conv_factor: float = 1):
        """Instanciate object.

        Args:
            device_address (str): Device's I2C address. Two digit hex.
            bus (int): I2C bus to use.
            gain (int): Gain of chip. See datasheet.
            unit [0, 1, 2]: 0 for return number of bins, 1 for return voltages, 2 for return current (voltage * curr_conv_factor)
            current_conv_factor (float): if unit is 2, measured voltages are multiplied with this factor to get a current reading
        """
        self.device_address = self.check_and_convert_hex(device_address)
        self.name = name
        self.bus = bus
        self.adc = Adafruit_ADS1x15.ADS1115(
            address=self.device_address, busnum=self.bus
        )
        self.gain = None
        self.set_gain(gain)
        self.set_unit(unit)
        self.current_conv_factor = current_conv_factor

    def check_and_convert_hex(self, hex: str):
        """Check two-digit hex and convert to integer.

        Args:
            hex (str): Two-digit hex to be converted.

        Returns:
            int: Integer value of hex.
        """
        if len(hex) != 2:
            raise Exception("Address wrong length.")
        return int(hex, 16)

    def set_unit(self, unit):
        """Set unit of ADC.

        Args:
            unit [0, 1, 2]: 0 for number of bins, 1 for voltage, 2 for current (voltage times current_conv_factor)
        """
        if unit in [0, 1, 2]:
            self.unit = unit
        else:
            print("Unit has to be 0 (number of bins), 1 (voltages) or 2 (current).")

    def set_gain(self, gain, verbose=False):
        """Set gain of ADC.

        Args:
            gain (int):
                (2/3 = +/-6.144V)
                   1 = +/-4.096V
                   2 = +/-2.048V
                   4 = +/-1.024V
                   8 = +/-0.512V
                  16 = +/-0.256V
                  (Vcc must be > AIN)
            verbose (bool): Verbose output.
        """
        if gain in self.gain_limits:
            self.gain = gain
        else:
            print(
                "Gain has to be 2/3 = +/-6.144V \n 1 = +/-4.096V \n 2 = +/-2.048V \n 4 = +/-1.024V \n 8 = +/-0.512V \n 16 = +/-0.256V"
            )

        if verbose:
            self.get_gain()

    def get_gain(self):
        """Print gain of ADC with voltage limits.

        Args:
            gain (int):
                (2/3 = +/-6.144V)
                   1 = +/-4.096V
                   2 = +/-2.048V
                   4 = +/-1.024V
                   8 = +/-0.512V
                  16 = +/-0.256V
        """
        print(f"Gain set to {self.gain}.")
        print(f"Limits: +/- {self.gain_limits[self.gain]}")

    def get_channels(self, channels=[0, 1, 2, 3]):
        """Read channels.

        Args:
            channels (list of int): Input channels to read. List containing digits 0, 1, 2, 3.

        Returns:
            list of floats: Measurements as number of bins, voltages or currents, depending on value of self.unit.
        """
        values = [self.adc.read_adc(channel, gain=self.gain) for channel in channels]

        if self.unit == 1:
            # voltages
            values = [
                value * self.gain_limits[self.gain] / (self.max_bin / 2) for value in values
            ]
        elif self.unit == 2:
            # currents
            values = [
                value * self.gain_limits[self.gain] / (self.max_bin / 2) * self.current_conv_factor for value in values
            ]
        return values


def log_data_func(data_adcs):
    with open("Data/adcs.data", "a") as file:
        current_time = time.localtime()
        current_time = time.strftime("%H:%M:%S", current_time)
        file.write(current_time + "\t" + "\t".join(data_adcs) + "\n")


def read_adcs(adcs, interval: float = 1, log_interval = 3):
    unit_dic = {0: "# Bins", 1: "V", 2: "A"}

    # header shown only once at top
    header1 = [f"ADC {adc.device_address} [{unit_dic[adc.unit]}]" for adc in adcs]
    # header with column names
    header2 = []
    for adc in adcs:
        header2.extend([f"{adc.name} {i}" for i in range(1,5)])

    width = 6
    print(tp.header(header1, width = 4 * (width + 2) + 1))
    print(tp.header(header2, width = width))

    log_counter = 0

    while True:

        # print header again after every 10 rows
        for i in range(10):
            log_counter += 1
            time.sleep(interval)
            data_adcs = []
            for adc in adcs:
                data_adcs.extend(adc.get_channels())
            data_adcs = np.round(np.array(data_adcs), 2)
            data_adcs = [f"{value:.2f}" for value in data_adcs]
            print(tp.row(data_adcs, width=width), flush=True)

            if log_counter >= log_interval:
                log_data_func(data_adcs)
                log_counter = 0
        print(tp.header(header2, width = width))
