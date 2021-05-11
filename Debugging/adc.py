import sys
import time
sys.path.append(".")
from Modules.adc_ads1115 import ADC, ADCS

adc_1 = ADC("48")
adc_2 = ADC("4a")


while True:
    print(adc_1.get_channels())
    #  print(adc_2.get_channels())
    time.sleep(1)
