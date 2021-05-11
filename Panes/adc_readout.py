import sys
sys.path.append(".")
from Modules.adc_ads1115 import ADC, ADCS

# address assignment checked
adc_vmupix = ADC("48")
adc_current = ADC("49")
adc_vdiode = ADC("4a")

#  adcs = ADCS([adc_vmupix, adc_vdiode])
adcs = ADCS([adc_vdiode, adc_vmupix])
adcs.get_channels(interval = 1, current_conversion_factor = 4 / 0.1811)
