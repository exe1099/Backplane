import sys
sys.path.append(".")
from Devices.adc_ads1115 import ADC, ADCS
import os

os.system("clear")

# address assignment checked for minicrate v2
adc_vmupix = ADC("48", "VMup")
adc_current = ADC("49", "Curr", unit = 2, current_conv_factor= 15 / 0.61)
        # theoretical factor: 10 / 0.4
adc_vdiode = ADC("4a", "VDio")

adcs = ADCS([adc_current, adc_vmupix, adc_vdiode])
# adcs = ADCS([adc_current, adc_vdiode])
adcs.get_channels(interval = 1)
