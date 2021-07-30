import sys
sys.path.append(".")
from Devices.adc_ads1115 import ADC, ADCS
import os

os.system("clear")

# address assignment checked for minicrate v2
adc_vmupix = ADC("48", "VMup")
adc_current = ADC("49", "Curr", unit = 2, current_conv_factor= 25)
        # units:    0 for bins
        #           1 for voltage
        #           2 for current
        # theoretical factor: 25
        # experimental board 10: 24.6
adc_vdiode = ADC("4a", "VDio")

adcs = ADCS([adc_current])
# adcs = ADCS([adc_current, adc_vdiode])


adcs.get_channels(interval = 1)
