from Modules.adc_ads1115 import ADC, ADCS

# address assignment checked
adc_current = ADC("48")
adc_vdiode = ADC("49")
adc_vmupix = ADC("4b")

adcs = ADCS([adc_current, adc_vmupix])
adcs.get_channels(interval = 1, current_conversion_factor = 4 / 0.1811)
