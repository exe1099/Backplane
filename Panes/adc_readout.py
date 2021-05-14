import sys
sys.path.append(".")
from Devices.adc_ads1115 import ADC, ADCS

# address assignment checked for minicrate v2
adc_vmupix = ADC("48", "VMupix")
adc_current = ADC("49", "Current", unit = 2, current_conv_factor= 4 / 0.1811)
        # theoretical factor: 10 / 0.4
adc_vdiode = ADC("4a", "VDiode")

adcs = ADCS([adc_current, adc_vmupix, adc_vdiode])
adcs.get_channels(interval = 1)
