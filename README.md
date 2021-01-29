# Backplane
Code for running the prototype backplane


Installation
============
* tps_pmbus module
    `pip3 install smbus2`

* Adafruit ADS1x15 library
    `pip3 install adafruit-ads1x15`

* configurate i2c bus 4 on pins 23 (sda) and 24 (scl)
    * in /boot/config.txt uncomment/add:
        `dtparam=i2c_arm=on
        dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24`
