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
""" Look at me! I'm a module docstring. """
import wiringpi
# from time import time, localtime, struct_time, mktime

# GPIO constants
_R5222_PIN = 22
_LE_PIN = 3

_I2C_Address = 0x68
_I2C_Flush = 0

# NCS31X values
_DEBOUNCE_DELAY = 150
_TOTAL_DELAY = 17

UP_BUTTON_PIN = 1
DOWN_BUTTON_PIN = 4
MODE_BUTTON_PIN = 5

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

UPPER_DOTS_MASK = 0x80000000
LOWER_DOTS_MASK = 0x40000000

LEFT_REPR_START = 5
LEFT_BUFFER_START = 0
RIGHT_REPR_START = 2
RIGHT_BUFFER_START = 4

_NCSHV5222 = None

_gpio = None
config = None

#
# display controls
#

def blank():
    wiringpi.digitalWrite(_LE_PIN, wiringpi.LOW)

def unblank():
    wiringpi.digitalWrite(_LE_PIN, wiringpi.HIGH)

def update_backlight(color):
    wiringpi.softPwmWrite(_RED_LIGHT_PIN, color[0])
    wiringpi.softPwmWrite(_GREEN_LIGHT_PIN, color[1])
    wiringpi.softPwmWrite(_BLUE_LIGHT_PIN, color[2])
#
# RTC functions
#

#
# think: consolidate? does this even work?
#

def write_rtc_time(tm):
    def _dec_to_bcd(val):
        return (int(val / 10) * 16) + (val % 10)

    def update_rtc_hour(tm):
        wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)
        wiringpi.wiringPiI2CWriteReg8(_gpio,
                                      _HOUR_REGISTER,
                                      _dec_to_bcd(tm.tm_hour))
        wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)

    def update_rtc_minute(tm):
        wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)
        wiringpi.wiringPiI2CWriteReg8(_gpio,
                                      _MINUTE_REGISTER,
                                      _dec_to_bcd(tm.tm_min))
        wiringpi.wiringPiI2CWriteReg8(_gpio,
                                      _HOUR_REGISTER,
                                      _dec_to_bcd(tm.tm_hour))
        wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)

    def reset_rtc_second():
        wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)
        wiringpi.wiringPiI2CWriteReg8(_gpio, _SECOND_REGISTER, 0)
        wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)

    wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)
    wiringpi.wiringPiI2CWriteReg8(_gpio,
                                  _SECOND_REGISTER,
                                  _dec_to_bcd(tm.tm_sec))
    wiringpi.wiringPiI2CWriteReg8(_gpio,
                                  _MINUTE_REGISTER,
                                  _dec_to_bcd(tm.tm_min))
    wiringpi.wiringPiI2CWriteReg8(_gpio,
                                  _HOUR_REGISTER,
                                  _dec_to_bcd(tm.tm_hour))
    wiringpi.wiringPiI2CWriteReg8(_gpio,
                                  _WEEK_REGISTER,
                                  _dec_to_bcd(tm.tm_wday))
    wiringpi.wiringPiI2CWriteReg8(_gpio,
                                  _DAY_REGISTER,
                                  _dec_to_bcd(tm.tm_day))
    wiringpi.wiringPiI2CWriteReg8(_gpio,
                                  _MONTH_REGISTER,
                                  _dec_to_bcd(tm.tm_month))
    wiringpi.wiringPiI2CWriteReg8(_gpio,
                                  _YEAR_REGISTER,
                                  _dec_to_bcd(tm.tm_year))
    wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)

# check the clock skew, if it's off by more than a little bit,
# sync to the host's time

def sync_time():
    def _bcd_to_dec(val):
        return ((val >> 4) * 10) + (val & 0xf)

    def _hour12():
        tm_hour = _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio,
                                                           _HOUR_REGISTER))
        if config['12hour'] and tm_hour > 12:
            tm_hour -= 12

        return tm_hour

    wiringpi.wiringPiI2CWrite(_gpio, _I2C_Flush)

    now = (_bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio,
                                                    _YEAR_REGISTER)) + 1900,
           _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio,
                                                    _MONTH_REGISTER)) + 1,
           _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio,
                                                    _DAY_REGISTER)) + 1,
           _hour12(),
           _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio,
                                                    _MINUTE_REGISTER)),
           _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio,
                                                    _SECOND_REGISTER)),
           _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio,
                                                    _WEEK_REGISTER)),
           1,
           -1)

    return now

#
# stuff the tubes
#

def display(tubes):
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

    wiringpi.pinMode(_LE_PIN, wiringpi.OUTPUT)
    wiringpi.digitalWrite(_LE_PIN, wiringpi.LOW)

    display_ = tubes
    if _NCSHV5222:
        reverse = rev_bits(tube_to_bits(display))

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
    wiringpi.digitalWrite(_LE_PIN, wiringpi.HIGH)

def init_pin(pin):
    wiringpi.pinMode(pin, wiringpi.INPUT)
    wiringpi.pullUpDnControl(pin, wiringpi.PUD_UP)

#
# events
#

# think: this is ugly
def func_mode():
    if (wiringpi.millis() - func_mode.debounce) > _DEBOUNCE_DELAY:
        print('MODE button was pressed.')
        func_mode.debounce = wiringpi.millis()
func_mode.debounce = 0

def func_up():
    if (wiringpi.millis() - func_up.debounce) > _DEBOUNCE_DELAY:
        print('UP button was pressed.')
        func_up.debounce = wiringpi.millis()
func_up.debounce = 0

def func_down():
    if (wiringpi.millis() - func_down.debounce) > _DEBOUNCE_DELAY:
        print('DOWN button was pressed.')
        func_down.debounce = wiringpi.millis()
func_down.debounce = 0

def ncs31x(conf_dict):
    global _NCSHV5222    # death to globals
    global _gpio
    global config

    config = conf_dict

    wiringpi.wiringPiSetup()

    # wiringpi.softToneCreate(BUZZER_PIN)
    # wiringpi.softToneWrite(BUZZER_PIN, 1000)

    wiringpi.softPwmCreate(_RED_LIGHT_PIN, 0, _MAX_POWER)
    wiringpi.softPwmCreate(_GREEN_LIGHT_PIN, 0, _MAX_POWER)
    wiringpi.softPwmCreate(_BLUE_LIGHT_PIN, 0, _MAX_POWER)

    if conf_dict and conf_dict['back_light']:
        update_backlight(conf_dict['back_light'])

    # open the I2C bus to the NCS31X device
    _gpio = wiringpi.wiringPiI2CSetup(_I2C_Address)
    if wiringpi.wiringPiSPISetupMode(0, 2000000, 2):
        return

    # initialize the display
    wiringpi.pinMode(_R5222_PIN, wiringpi.INPUT)
    wiringpi.pullUpDnControl(_R5222_PIN, wiringpi.PUD_UP)

    _NCSHV5222 = not wiringpi.digitalRead(_R5222_PIN)
