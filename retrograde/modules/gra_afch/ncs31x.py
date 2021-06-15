##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## NCS31X device driver
##
###########

"""

     Look at me! I'm a module docstring.

"""

import wiringpi
from time import struct_time

class Ncs31x:
    """NCS31X class
    """

    # GPIO constants
    _R5222_PIN = 22
    _LE_PIN = 3

    _I2C_ADDRESS = 0x68
    _I2C_FLUSH = 0

    # NCS31X values
    _DEBOUNCE_DELAY = 150
    _TOTAL_DELAY = 17

    _BUZZER_PIN = 0

    _SECOND_REGISTER = 0x0
    _MINUTE_REGISTER = 0x1
    _HOUR_REGISTER = 0x2
    _WEEK_REGISTER = 0x3
    _DAY_REGISTER = 0x4
    _MONTH_REGISTER = 0x5
    _YEAR_REGISTER = 0x6

    _MAX_POWER = 100
    _RED_LIGHT_PIN = 28
    _GREEN_LIGHT_PIN = 27
    _BLUE_LIGHT_PIN = 29

    # externs
    UP_BUTTON_PIN = 1
    DOWN_BUTTON_PIN = 4
    MODE_BUTTON_PIN = 5

    UPPER_DOTS_MASK = 0x80000000
    LOWER_DOTS_MASK = 0x40000000

    LEFT_REPR_START = 5
    LEFT_BUFFER_START = 0
    RIGHT_REPR_START = 2
    RIGHT_BUFFER_START = 4

    # class variables
    _ncshv5222 = None
    _gpio = None
    _conf_dict = None

    def blank(self, state):
        """power off the display
        """

        wiringpi.digitalWrite(self._LE_PIN,
                              wiringpi.LOW if state else wiringpi.HIGH)

    def backlight(self, color):
        """change the backlight color
        """

        wiringpi.softPwmWrite(self._RED_LIGHT_PIN, color[0])
        wiringpi.softPwmWrite(self._GREEN_LIGHT_PIN, color[1])
        wiringpi.softPwmWrite(self._BLUE_LIGHT_PIN, color[2])

    def write_rtc(self, tm):
        """write the RTC

           from a time struct
        """

        def _dec_to_bcd(val):
            return (int(val / 10) * 16) + (val % 10)

        wiringpi.wiringPiI2CWrite(self._gpio, self._I2C_FLUSH)
        wiringpi.wiringPiI2CWriteReg8(self._gpio,
                                      self._SECOND_REGISTER,
                                      _dec_to_bcd(tm.tm_sec))
        wiringpi.wiringPiI2CWriteReg8(self._gpio,
                                      self._MINUTE_REGISTER,
                                      _dec_to_bcd(tm.tm_min))
        wiringpi.wiringPiI2CWriteReg8(self._gpio,
                                      self._HOUR_REGISTER,
                                      _dec_to_bcd(tm.tm_hour))
        wiringpi.wiringPiI2CWriteReg8(self._gpio,
                                      self._WEEK_REGISTER,
                                      _dec_to_bcd(tm.tm_wday))
        wiringpi.wiringPiI2CWriteReg8(self._gpio,
                                      self._DAY_REGISTER,
                                      _dec_to_bcd(tm.tm_mday))
        wiringpi.wiringPiI2CWriteReg8(self._gpio,
                                      self._MONTH_REGISTER,
                                      _dec_to_bcd(tm.tm_mon))
        wiringpi.wiringPiI2CWriteReg8(self._gpio,
                                      self._YEAR_REGISTER,
                                      _dec_to_bcd(tm.tm_year))
        wiringpi.wiringPiI2CWrite(self._gpio, self._I2C_FLUSH)

    def read_rtc(self):
        """read the RTC
            return a struct_time()
        """

        def _bcd_to_dec(val):
            return ((val >> 4) * 10) + (val & 0xf)

        def _hour12():
            tm_hour = _bcd_to_dec(
                    wiringpi.wiringPiI2CReadReg8(self._gpio,
                                                 self._HOUR_REGISTER))
            if self._conf_dict['12hour'] and tm_hour > 12:
                tm_hour -= 12

            return tm_hour

        wiringpi.wiringPiI2CWrite(self._gpio, self._I2C_FLUSH)

        now = (_bcd_to_dec(wiringpi.wiringPiI2CReadReg8(self._gpio,
                                                        self._YEAR_REGISTER))
               + 1900,
               _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(self._gpio,
                                                        self._MONTH_REGISTER)),
               _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(self._gpio,
                                                        self._DAY_REGISTER)),
               _hour12(),
               _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(self._gpio,
                                                        self._MINUTE_REGISTER)),
               _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(self._gpio,
                                                        self._SECOND_REGISTER)),
               _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(self._gpio,
                                                        self._WEEK_REGISTER)),
               1,
               -1)

        return struct_time(now)

    def display(self, tubes):
        """put the tube representation into the tubes
        """

        def rev_bits(nval):
            reversed_ = 0
            i = 0
            while i < 64:
                if nval & 1 << i:
                    reversed_ |= 1 << (63 - i)

            return reversed_

        def tube_to_bits(tubes):
            bits = 0
            for n in range(8):
                bits |= tubes[n]
                bits <<= 8

            return bits

        wiringpi.pinMode(self._LE_PIN, wiringpi.OUTPUT)
        wiringpi.digitalWrite(self._LE_PIN, wiringpi.LOW)

        display_ = tubes
        if self._ncshv5222:
            reverse = rev_bits(tube_to_bits(display_))

            display_[4] = reverse
            display_[5] = reverse >> 8
            display_[6] = reverse >> 16
            display_[7] = reverse >> 24
            display_[0] = reverse >> 32
            display_[1] = reverse >> 40
            display_[2] = reverse >> 48
            display_[3] = reverse >> 56

        buf = bytes(display_)

        wiringpi.wiringPiSPIDataRW(0, buf)
        wiringpi.digitalWrite(self._LE_PIN, wiringpi.HIGH)

    def init_pin(self, pin):
        """set a GPIO pin to input and pulled-up
        """

        wiringpi.pinMode(pin, wiringpi.INPUT)
        wiringpi.pullUpDnControl(pin, wiringpi.PUD_UP)

    # think: boy howdy, this is ugly
    def func_mode(self):
        """run the rotor thread
        """

        if (wiringpi.millis() - self.func_mode.debounce) > self._DEBOUNCE_DELAY:
            print('MODE button was pressed.')
            self.func_mode.debounce = wiringpi.millis()
    func_mode.debounce = 0

    def func_up(self):
        """run the rotor thread
        """
        if (wiringpi.millis() - self.func_up.debounce) > self._DEBOUNCE_DELAY:
            print('UP button was pressed.')
            self.func_up.debounce = wiringpi.millis()
    func_up.debounce = 0

    def func_down(self):
        """run the rotor thread
        """

        if (wiringpi.millis() - self.func_down.debounce) > self._DEBOUNCE_DELAY:
            print('DOWN button was pressed.')
            self.func_down.debounce = wiringpi.millis()
    func_down.debounce = 0

    def __init__(self, conf_dict):
        """initialize an ncs31x object
        """

        self._conf_dict = conf_dict

        wiringpi.wiringPiSetup()

        # wiringpi.softToneCreate(BUZZER_PIN)
        # wiringpi.softToneWrite(BUZZER_PIN, 1000)

        wiringpi.softPwmCreate(self._RED_LIGHT_PIN, 0, self._MAX_POWER)
        wiringpi.softPwmCreate(self._GREEN_LIGHT_PIN, 0, self._MAX_POWER)
        wiringpi.softPwmCreate(self._BLUE_LIGHT_PIN, 0, self._MAX_POWER)

        if conf_dict and conf_dict['back_light']:
            self.backlight(conf_dict['back_light'])

        # open the I2C and SPI busses to the NCS31X device
        self._gpio = wiringpi.wiringPiI2CSetup(self._I2C_ADDRESS)
        if wiringpi.wiringPiSPISetupMode(0, 2000000, 2) < 0:
            assert False

        # initialize the display
        wiringpi.pinMode(self._R5222_PIN, wiringpi.INPUT)
        wiringpi.pullUpDnControl(self._R5222_PIN, wiringpi.PUD_UP)

        self._ncshv5222 = not wiringpi.digitalRead(self._R5222_PIN)
