import sys
sys.path.append(".")
from Devices.adc_ads1115 import ADC, read_adcs
import os

os.system("clear")

# address assignment checked for minicrate v2
# units:    0 for bins
#           1 for voltage
#           2 for current
adc_vmupix = ADC("48", "VMup")
adc_current = ADC("49", "Curr", unit = 2, current_conv_factor= 25)
    # theoretical factor: 25
    # experimental board 10: 24.6
adc_vdiode = ADC("4a", "VDio")

read_adcs([adc_current], interval=1)
