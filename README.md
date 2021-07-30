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
 * configurate i2c bus 3 on pins 7 (sda) and 8 (scl) (normally not needed; for additional external devices)
        `dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=7,i2c_gpio_scl=8`

Pins Pi
=======
* TPSs: bus 1 (sda1 to pin 2, scl1 to pin 3)
* ADCs: bus 4 (sda2 to 23, scl2 to 24) (see above)

Controlling Boards
==================
* start session with ./start_session.sh
* this is now running a tmux session with prefix set to control + w (press simultaniously)
* to exit the session (for example if you turned off the powersupply etc) press prefix followed by x
  (so ctrl + w simultaniously, let go and then press x)
* call object with tpsXX.method()
* function examples
    * toggle_on_off_bit()
        * 0: off
        * 1: on
        * nothing/-1: toggle
    * toggle_en_pin_behaviour(n)
        * 0: ignore
        * 1: on
        * nothing/-1: toggle
    * get_switching_freq()
    * set_switching_feq(n)
        * 0-7
    * get_status_word()
    * clear_faults()
    * status()
    * stats()
    * set_UVLO_threshold(n)
        * 0-3
    * get_UVLO_threshold()
    * load_defaults()
        * 1 MHz, ignore enable pin, FCCM, converter off (on with toggle_converter())
    * toggle_fccm(n)
        * 0: DCM (discontinuous conduction mode)
        * 1: FCCM (forced continuous conduction mode)
        * nothing/-1: toggle
* old stuff (just ignore)
    * edit control_board.py and uncomment/add lines including device I2C address
    * run `python3 -i control_boards.py` for interactive python session

Temperature Reading
===================
* to activate the one wire temp interface on the RaspberryPi, run ./activate_temp_sensors_interface.sh
    * only need to do that once after every restart
* a dictionary converting the unique ID of the temp sensor to a board address can be found under Devices/ds18b20.py
    * add entry here when adding/changing temp sensor

Reading ADCS
============
* run `python3 adc_readout.py`
* to change parameters edit adc_readout.py 
    `def get_channels(self, interval: float = 0, voltages: bool = True): ...`

Layouts
=======
* even_horizontal
