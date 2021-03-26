#!//usr/bin/python3

import argparse
from smbus2 import SMBus


class TPS:
    def __init__(self, device_address: str = "1b", bus: int = 1):
        """Initialise object.

        Args:
            device_address (str): Device's I2C address. Two digit hex.
            bus (int): I2C bus to use.
        """
        self.device_address = self.check_and_convert_hex(device_address)
        self.bus = bus
        # check if communication possible
        try:
            self.get_byte("01", verbose=False)
        except IOError:
            raise IOError(f"No communication with device under {self.device_address}")

        print(f"TPS object instantiated. Call with tps{device_address}.method()")

    def get_byte(self, register: str, verbose=True):
        """Read register.

        Args:
            register (str): Register to read from. Two digit hex.
            verbose (bool): Verbose output.

        Returns:
            int: Value of byte read from register (as integer).
        """
        register = self.check_and_convert_hex(register)

        with SMBus(self.bus) as bus:
            byte = bus.read_byte_data(self.device_address, register)  # returned as int

        if verbose:
            print("Hex: " + str.upper(format(byte, "02x")))
            byte_bin = format(byte, "08b")
            print(
                "Binary: "
                + byte_bin[0:2]
                + " "
                + byte_bin[2:4]
                + " "
                + byte_bin[4:6]
                + " "
                + byte_bin[6:]
            )

        return byte

    def get_word(self, register: str, verbose=True):
        """Read word (two byte).

        Args:
            register (str): Register to read from. Two digit hex.
            verbose (bool): Verbose output.

        Returns:
            int: Value of word read from register (as integer).
        """
        register = self.check_and_convert_hex(register)

        with SMBus(self.bus) as bus:
            word = bus.read_word_data(self.device_address, register)

        if verbose:
            print("Hex: " + str.upper(format(word, "04x")))
            word_bin = format(word, "016b")
            print("Binary: " + word_bin)

        return word

    def set_byte(self, register: str, byte: str):
        """Write byte in register.

        Args:
            register (str): Register to write to. Two digit hex.
            byte (str): Byte to write. Can be two digit hex or eight digit binary.
        """
        register = self.check_and_convert_hex(register)

        if len(byte) == 2:
            byte = int(byte, 16)
        elif len(byte) == 8:
            byte = int(byte, 2)
        else:
            print("Data to be written must be hex or binary (e.g. 1f or 01010101).")

        with SMBus(self.bus) as bus:
            # b = bus.write_byte_data(self.device_address, register, byte)
            bus.write_byte_data(self.device_address, register, byte)

    def send_byte(self, byte: str):
        """Send byte (i.e. a command).

        Args:
            byte (str): The byte to send. Must be two digit hex.
        """
        with SMBus(self.bus) as bus:
            bus.write_byte(self.device_address, int(byte, 16))

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

    def set_bit(self, register: str, n_bit: int, value: int = 1):
        """Write single bit in register at position n_bit.

        Args:
            register (str): Register to change.
            n_bit (int): Position of bit to change (most right bit --> index 0).
            value (int): 0 or 1, or -1 to toggle bit.

        Returns:
            int: Written bit.
        """
        # reverse for proper bit numbering [7 to 0]
        temp = list(format(self.get_byte(register, verbose=False), "08b"))[::-1]
        # set bit
        temp[n_bit] = (
            str(value) if value in [0, 1] else str(int(not (int(temp[n_bit]))))
        )
        temp = "".join(temp)
        self.set_byte(register, temp[::-1])
        return temp[n_bit]

    ### Shortcut Functions ###
    def toggle_converter(self, i: int = -1):
        written = self.set_bit("01", 7, i)
        print("Converter on: " + written)

    def get_converter(self):
        byte = self.get_byte("01", verbose=False)
        print("Converter on: " + format(byte, "08b")[0])

    def toggle_en_pin_behaviour(self, i: int = -1):
        written = self.set_bit("02", 2, i)
        print("Enable pin behaviour: " + written)

    def toggle_on_off_bit_behaviour(self, i: int = -1):
        written = self.set_bit("02", 3, i)
        print("On-off bit behaviour: " + written)

    def set_switch_freq(self, i: int = 7):
        byte = "b" + str(i)
        self.set_byte("d3", byte)

    def get_switch_freq(self):
        byte = format(self.get_byte("d3", verbose=False), "08b")
        value = int(byte[5:], 2)

        dic = {0: 275, 1: 325, 2: 425, 3: 525, 4: 625, 5: 750, 6: 850, 7: 1000}
        print(f"Switching Freq.: {dic[value]} kHz")

    def get_write_protect(self):
        byte = self.get_byte("10", verbose=False)
        if byte == 0:
            print("Write protection: off")
        else:
            print("Write protection set to: " + format(byte, "08b"))

    def get_status_word(self, verbose=True):
        word = format(self.get_word("79", verbose=False), "016b")
        print("Status word: " + word)

        if verbose:
            flags_set = [i for i in range(len(word)) if word[i] == "1"]
            flag_dic = {
                0: "Output voltage fault or warning has occured (latched).",
                1: "Output current fault or warning has occured (latched).",
                2: "Input voltage fault or warning has occured (latched).",
                3: "MFR (not implemented, should always be 0).",
                4: "PGOOD is low (status).",
                5: "FANS (not implemented, should always be 0).",
                6: "OTHER (not implemented, should always be 0).",
                7: "UNKNOWN (not implemented, should always be 0).",
                8: "Busy (not implemented, should always be 0).",
                9: "Not providing power to output voltage (status).",
                10: "Output voltage overvoltage fault has occured (latched).",
                11: "Output current overcurrent fault has occured (latched).",
                12: "Input voltage is below UVLO turn-on threshold (latched).",
                13: "Over temperature fault has occured (latched).",
                14: "Communication, memory or logic fault has occured (latched).",
                15: "More faults in high byte.",
            }
            for i in flags_set:
                print(flag_dic[i])

    def status(self):
        self.get_converter()
        self.get_status_word()

    def stats(self):
        # self.read_write_protect()
        # self.read_soft_start_config()
        self.get_UVLO_threshold()
        self.get_switch_freq()
        self.get_converter()
        self.get_status_word()

    def toggle_FCCM(self, i: int = -1):
        """Switch between discontinuous (DCM) and forced continuous conduction mode and (FCCM).
        """
        written = self.set_bit("D2", 0, i)
        print("FCCM: " + written)

    def get_soft_start_config(self):
        byte = format(self.get_byte("d2", verbose=False), "08b")
        sst = 2 ** int(byte[4:6], 2)
        print(f"Soft-start time: {sst}ms")
        hiccup = not bool(int(byte[6]))
        print(f"Hiccup after UV: {hiccup}")
        fccm = bool(int(byte[7]))
        print(f"Forced continuous conduction mode: {fccm}")

    def get_UVLO_threshold(self):
        byte = format(self.get_byte("d6", verbose=False), "08b")
        dic = {
            "000": 10.2,
            "001": 10.2,
            "010": 10.2,
            "011": 10.2,
            "101": 4.25,
            "110": 6,
            "111": 8.1,
        }
        print(f"UVLO threshold: {dic[byte[5:]]} V")

    def set_UVLO_threshold(self, i: int = 0):
        """Write UVLO threshold.
        (this is undervoltage for TPS VDD, not power V_IN)

        Args:
        i (int): [0-3], 0: 4.25 V, 1: 6 V, 2: 8.1 V, 3: 10.2 V
        """
        dic = {0: "101", 1: "110", 2: "111", 3: "000"}
        self.set_byte("d6", "00000" + dic[i])
        self.get_UVLO_threshold()

    def load_defaults(self):
        self.toggle_en_pin_behaviour(0)
        self.toggle_on_off_bit_behaviour(1)
        self.get_write_protect()
        self.toggle_FCCM(1)
        self.get_soft_start_config()
        self.get_UVLO_threshold()
        self.set_switch_freq(7)
        self.get_switch_freq()
        self.toggle_converter(0)
        self.get_status_word()
        print("Default settings loaded!")

    ### Commands ###
    def clear_faults(self):
        self.send_byte("03")

    def store_defaults(self):
        self.send_byte("11")

    def restore_defaults(self):
        self.send_byte("12")

