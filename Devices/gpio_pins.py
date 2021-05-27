from gpiozero import LED
from gpiozero import Button

# connected pins (slot 1, slot 2, slot 3, slot 4)
# enable switch: 22, 27, 17, 4
# DQ: 14
# ALERT1: 15
# ALERT2: 18 (?)
# PGOOD: 21, 20, 16, 12
# TINTERLOCK: 26, 19, 13, 6

class PGOOD:
    # PGOOD: 21, 20, 16, 12
    def __init__(self):
        self.inputs = [Button(21, pull_up = False), 
                        Button(20, pull_up = False),
                        Button(16, pull_up = False),
                        Button(12, pull_up = False)]
    def get_values(self):
        values = [input.is_pressed for input in self.inputs]
        return values

class TINTERLOCK:
    # TINTERLOCK: 26, 19, 13, 6
    def __init__(self):
        self.inputs = [Button(26, pull_up = False), 
                        Button(19, pull_up = False),
                        Button(13, pull_up = False),
                        Button(6, pull_up = False)]
    def get_values(self):
        values = [input.is_pressed for input in self.inputs]
        return values

class ALERT:
    def __init__(self):
        self.inputs = [Button(15, pull_up = False),
                        Button(18, pull_up = False)]
    
    def get_values(self):
        values = [input.is_pressed for input in self.inputs]
        return values

class ENABLE_SWITCH:
    def __init__(self):
        self.switches = [LED(22, initial_value = False), 
                         LED(27, initial_value = False), 
                         LED(17, initial_value = False), 
                         LED(4, initial_value = False)]
        # enable low at start
    
    def set(self, slot : int, bit : int):
        if slot not in range(1, 5):
            print("Slot must be 1, 2, 3 or 4.")
            return None
        if bit not in [0, 1]:
            print("Second parameter must be 0 (switch open --> enable low) or 1 (switch closed --> enable high).")
            return None
        if bit:
            print("wrote")
            self.switches[slot - 1].on()
        else:
            self.switches[slot - 1].off()
        self.get()

    def get(self, verbose=True):
        state = [switch.value for switch in self.switches]
        if verbose:
            state_str = [str(i) for i in state]
            state_str = " ".join(state_str)
            print("State: " + state_str)
        else:
            return state



