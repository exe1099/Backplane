import time
import Adafruit_ADS1x15


class ADC:

    gain_limits = {1: 4.096, 2: 2.048, 4: 1.024, 8: 0.512, 16: 0.256}
    max_bin = 2 ** 16 - 1

    def __init__(self, device_address: str = "48", bus: int = 4, gain: int = 1):
        """Instanciate object.

        Args:
            device_address (str): Device's I2C address. Two digit hex.
            bus (int): I2C bus to use.
            gain (int): Gain of chip. See datasheet.
        """
        self.device_address = self.check_and_convert_hex(device_address)
        self.bus = bus
        self.adc = Adafruit_ADS1x15.ADS1115(
            address=self.device_address, busnum=self.bus
        )
        self.gain = None
        self.set_gain(gain)

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

    def set_gain(self, gain):
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
        """
        if gain in self.gain_limits:
            self.gain = gain
        else:
            print(
                "Gain has to be 2/3 = +/-6.144V \n 1 = +/-4.096V \n 2 = +/-2.048V \n 4 = +/-1.024V \n 8 = +/-0.512V \n 16 = +/-0.256V"
            )
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

    def get_channels(self, channels=[1], voltages: bool = True):
        """Read channels.

        Args:
            channels (list of int): Input channels to read. List containing digits 0, 1, 2, 3.
            voltages (bool): True to get voltages, False to get number of bins.

        Returns:
            list of floats: Read values as voltages or number of bins.
        """
        values = [self.adc.read_adc(channel, gain=self.gain) for channel in channels]

        if voltages:
            values = [
                value * self.gain_limits[self.gain] / ((2**16-1) / 2) for value in values
            ]
        return values


class ADCS:
    def __init__(self, adcs):
        """Instanciate object.

        Args:
            adcs (list of ADC): List with ADC objects.
        """
        self.adcs = adcs

    def get_channels(self, n_channels, interval: float = 0, voltages: bool = True):
        """Read channels.

        Args:
            channels (list of list of int): List of list of channels for each ADC.
            interval (float): Continous read with interval seconds between reads. 0 for single read.
            voltages (bool): True to get voltages, False to get number of bins.

        Returns:
        """
        print("|" + " | ".join([f"ADC {adc.device_address:()}" for adc in self.adcs]) + "|")

        for channels in n_channels:
            # print("|" + " | ".join([f"Channel {i}" for i in channels]) + "|", end="")
            print("| " + " | ".join([f"{i:6}" for i in channels]) + " |", end="")
        print("")
        print("-" * (len(channels) * 9 + 1))

        w = 0
        while (w < 10):
            w += 1
            n_values = [adc.get_channels(channels, voltages = True) for channels in n_channels]

            for values in n_values:
                print("| " + " | ".join([f"{i:6.3f}" for i in values]) + " |", end="")
            print("")

            time.sleep(interval)

            # print("-" * (len(channels) * 9 + 1))
            # if voltages:
            #     print("| " + " | ".join([f"{i:6.3f}" for i in values]) + " |")
            # else:
            #     print("| " + " | ".join([f"{i:6}" for i in values]) + " |")

if __name__ == "__main__":

    from adc_ads1115 import ADC

    adc = ADC()
    adcs = ADCS([adc])
    adcs.get_channels([[0, 1, 2, 3]], interval=0.5)
