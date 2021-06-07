#!//usr/bin/python3

# import argparse
from smbus2 import SMBus


class TPS:
    def __init__(self, device_address: str = "1b", bus: int = 1):
        """Initialise object.

        Args:
            device_address (str): Device's I2C address. Two digit hex.
            bus (int): I2C bus to use.
        """
        self.device_address = self.check_and_convert_add(device_address)
        self.bus = bus
        # check if communication possible
        try:
            self.get_byte("01")
        except IOError:
            raise IOError(f"No communication with device under {device_address}")

        print(f"TPS object instantiated. Call with tps{device_address}.method()")

    def get_byte(self, register: str, integer=False, verbose=False):
        """Read register.

        Args:
            register (str): Register to read from. Two digit hex.
            integer (bool): Return byte as integer if true else as string (8 bit)
            verbose (bool): Verbose output.

        Returns:
            int: Value of byte read from register (as integer or as 8 bit string).
        """
        register = self.check_and_convert_add(register)

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
        else:
            if integer:
                return byte
            else:
                return format(byte, "08b")

    def get_word(self, register: str, verbose=True):
        """Read word (two byte).

        Args:
            register (str): Register to read from. Two digit hex.
            verbose (bool): Verbose output.

        Returns:
            int: Value of word read from register (as integer).
        """
        register = self.check_and_convert_add(register)

        with SMBus(self.bus) as bus:
            word = bus.read_word_data(self.device_address, register)

        if verbose:
            print("Hex: " + str.upper(format(word, "04x")))
            word_bin = format(word, "016b")
            print("Binary: " + word_bin)
        else:
            return word

    def set_byte(self, register: str, byte: str):
        """Write byte in register.

        Args:
            register (str): Register to write to. Two digit hex.
            byte (str): Byte to write. Must be two digit hex.
        """
        register = self.check_and_convert_add(register)

        if len(byte) != 2:
            raise Exception("Data to be written must be two digit hex.")

        with SMBus(self.bus) as bus:
            bus.write_byte_data(self.device_address, register, int(byte, 16))

    def send_byte(self, byte: str):
        """Send byte (i.e. a command).

        Args:
            byte (str): The byte to send. Must be two digit hex.
        """
        if len(byte) != 2:
            raise Exception("Data to be send must be two digit hex.")
            return None
        with SMBus(self.bus) as bus:
            bus.write_byte(self.device_address, int(byte, 16))

    def check_and_convert_add(self, hex: str):
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
        # list (strings immuatable) + reverse for proper bit numbering [7 to 0]
        data = list(self.get_byte(register))[::-1]
        # set bit
        value = str(value) if value in [0, 1] else str(int(not (int(data[n_bit]))))
        data[n_bit] = value
        data = "".join(data)  # back to string
        data = int(data[::-1], 2)  # to integer
        data = format(data, "02x")  # to hex
        self.set_byte(register, data)
        return value

    def get_bit(self, register: str, n_bit: int):
        """Read single bit from register at position n_bit.

        Args:
            register (str): Register to cread.
            n_bit (int): Position of bit to read (most right bit --> index 0).
        
        Returns:
            int: Read bit (0 or 1).
        """
        byte = self.get_byte(register)
        return byte[::-1][n_bit]

    ### Shortcut Functions ###
    def toggle_on_off_bit(self, i: int = -1, verbose=True):
        written = self.set_bit("01", 7, i)
        if verbose:
            print(f"On-off bit: {written}")
        else:
            return written

    def get_on_off_bit(self, verbose=True):
        state = self.get_bit("01", 7)
        if verbose:
            print(f"On-off Bit: {state}")
        else:
            return state

    def toggle_en_pin_behaviour(self, i: int = -1, verbose=True):
        written = self.set_bit("02", 2, i)
        if verbose:
            print(f"Enable pin behaviour: {written}")

    def get_en_pin_behaviour(self, verbose=True):
        state = self.get_bit("02", 2)
        if verbose:
            print(f"Enable pin behaviour: {state}")
        else:
            return state

    def toggle_on_off_bit_behaviour(self, i: int = -1, verbose=True):
        written = self.set_bit("02", 3, i)
        if verbose:
            print(f"On-off bit behaviour: {written}")

    def get_on_off_bit_behaviour(self, verbose=True):
        state = self.get_bit("02", 3)
        if verbose:
            print(f"On-off Bit Behaviour: {state}")
        else:
            return state

    def set_switch_freq(self, i: int = 7):
        if i not in range(1, 8):
            print("Value must be between 1 (275 kHz) and 7 (1 MHz)")
            return None
        self.set_byte("d3", format(i, "02x"))

    def get_switch_freq(self, verbose=True):
        dic = {0: 275, 1: 325, 2: 425, 3: 525, 4: 625, 5: 750, 6: 850, 7: 1000}
        byte = self.get_byte("d3")[5:]
        value = dic[int(byte, 2)]
        if verbose:
            print(f"Switching Freq.: {value} kHz")
        else:
            return value

    def get_write_protection(self, verbose=True):
        byte = self.get_byte("10")
        state = int(byte, 2)
        if verbose:
            if state == 0:
                print("Write protection: off")
            else:
                print(f"Write protection set to: {byte}")
        else:
            return state

    def get_status_word(self, verbose=True):
        word = format(self.get_word("79", verbose=False), "016b")
        translated = []
        print("Status word: " + word)
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
            translated.append(flag_dic[i])
        seperator = "\n"
        if verbose:
            print(seperator.join(translated))

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

    def toggle_fccm(self, i: int = -1, verbose=True):
        """Switch between discontinuous (DCM) and forced continuous conduction mode and (FCCM).
        """
        written = self.set_bit("d2", 0, i)
        if verbose:
            print("FCCM: " + written)

    def get_soft_start_config(self, verbose=True):
        byte = self.get_byte("d2")
        hiccup = int(not bool(int(byte[::-1][1])))
        fccm = int(byte[::-1][0])
        sst = 2 ** int(byte[4:6], 2)
        if verbose:
            print(f"Soft-start time: {sst}ms")
            print(f"Hiccup after UV: {hiccup}")
            print(f"Forced continuous conduction mode: {fccm}")
        else:
            return [sst, hiccup, fccm]

    def set_UVLO_threshold(self, i: int = 0):
        """Write UVLO threshold.
        (this is undervoltage for TPS VDD, not power V_IN)

        Args:
        i (int): [0-3], 0: 4.25 V, 1: 6 V, 2: 8.1 V, 3: 10.2 V
        """
        dic = {0: "101", 1: "110", 2: "111", 3: "000"}
        self.set_byte("d6", "00000" + dic[i])
        self.get_UVLO_threshold()

    def get_UVLO_threshold(self, verbose=True):
        byte = self.get_byte("d6")
        dic = {
            "000": 10.2,
            "001": 10.2,
            "010": 10.2,
            "011": 10.2,
            "101": 4.25,
            "110": 6,
            "111": 8.1,
        }
        value = dic[byte[5:]]
        if verbose:
            print(f"UVLO threshold: {value} V")
        else:
            return value

    def load_defaults(self):
        self.toggle_en_pin_behaviour(0, verbose=False)
        self.toggle_on_off_bit_behaviour(1, verbose=False)
        #  self.get_write_protect()
        self.toggle_fccm(1, verbose=False)
        #  self.get_soft_start_config()
        #  self.get_UVLO_threshold()
        self.set_switch_freq(7)
        #  self.get_switch_freq()
        self.toggle_on_off_bit(0, verbose=False)
        #  self.get_status_word()
        print("Default settings loaded!")

    ### Commands ###
    def clear_faults(self):
        self.send_byte("03")

    def store_defaults(self):
        self.send_byte("11")

    def restore_defaults(self):
        self.send_byte("12")

