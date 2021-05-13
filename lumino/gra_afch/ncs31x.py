##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## ncs31x driver
##
###########

import wiringpi
from time import time, localtime

# GPIO constants
_R5222_PIN = 22
_LE_PIN = 3

_I2CAdress = 0x68
_I2CFlush = 0

# NCS31X values
_DEBOUNCE_DELAY = 150
_TOTAL_DELAY = 17
_UP_BUTTON_PIN = 1
_DOWN_BUTTON_PIN = 4
_MODE_BUTTON_PIN = 5

_BUZZER_PIN = 0

_SECOND_REGISTER = 0x0
_MINUTE_REGISTER = 0x1
_HOUR_REGISTER = 0x2
_WEEK_REGISTER = 0x3
_DAY_REGISTER = 0x4
_MONTH_REGISTER = 0x5
_YEAR_REGISTER = 0x6

_RED_LIGHT_PIN = 28
_GREEN_LIGHT_PIN = 27
_BLUE_LIGHT_PIN = 29
_MAX_POWER = 100

_UPPER_DOTS_MASK = 0x80000000
_LOWER_DOTS_MASK = 0x40000000

_ncsHV5222 = None
    
def _bcd_to_dec(val):
    return (val / 16 * 10) + (val % 16)

def _dec_to_bcd(val):
    return (val / 10 * 16) + (val % 10)

def blank():
    wiringpi.digitalWrite(_RED_LIGHT_PIN, LOW)
    wiringpi.digitalWrite(_GREEN_LIGHT_PIN, LOW)
    wiringpi.digitalWrite(_BLUE_LIGHT_PIN, LOW)
    wiringpi.digitalWrite(_LE_PIN, LOW)
    update_backlight([0, 0, 0])
  
def unblank():
    wiringpi.digitalWrite(_RED_LIGHT_PIN, HIGH)
    wiringpi.digitalWrite(_GREEN_LIGHT_PIN, HIGH)
    wiringpi.digitalWrite(_BLUE_LIGHT_PIN, HIGH)
    wiringpi.digitalWrite(_LE_PIN, HIGH)

def init_pin(pin):
    wiringpi.pinMode(pin, INPUT)
    wiringpi.pullUpDnControl(pin, PUD_UP)

# this is ugly
def func_mode():
    if ((wiringpi.millis() - func_mode.debounce) > _DEBOUNCE_DELAY):
        print('MODE button was pressed.')
        func_mode.debounce = wiringpi.millis()
func_mode.debounce = 0
  
def func_up():
    if ((wiringpi.millis() - func_up.debounce) > DEBOUNCE_DELAY):
        print('UP button was pressed.')
        func_up.debounce = wiringpi.millis()
func_up.debounce = 0

def func_down():
    if ((wiringpi.millis() - func_down.debounce) > DEBOUNCE_DELAY):
        print('DOWN button was pressed.')
        func_down.debounce = wiringpi.millis()
func_down.debounce = 0

def update_rtc_hour(tm):
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, HOUR_REGISTER, _dec_to_bcd(tm.tm_hour))
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def update_rtc_minute(tm):
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, MINUTE_REGISTER, _dec_to_bcd(tm.tm_min))
    wiringpi.wiringPiI2CWriteReg8(_gpio, HOUR_REGISTER, _dec_to_bcd(tm.tm_hour))
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def reset_rtc_second():
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, SECOND_REGISTER, 0)
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def write_rtc_date(tm):
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, SECOND_REGISTER, _dec_to_bcd(tm.tm_sec))
    wiringpi.wiringPiI2CWriteReg8(_gpio, MINUTE_REGISTER, _dec_to_bcd(tme.tm_min))
    wiringpi.wiringPiI2CWriteReg8(_gpio, HOUR_REGISTER, _dec_to_bcd(tm.tm_hour))
    wiringpi.wiringPiI2CWriteReg8(_gpio, WEEK_REGISTER, _dec_to_bcd(tm.tm_wday))
    wiringpi.wiringPiI2CWriteReg8(_gpio, DAY_REGISTER, _dec_to_bcd(tm.tm_day))
    wiringpi.wiringPiI2CWriteReg8(_gpio, MONTH_REGISTER, _dec_to_bcd(tm.tm_month))
    wiringpi.wiringPiI2CWriteReg8(_gpio, YEAR_REGISTER, _dec_to_bcd(tm.tm_year))
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def get_rtc_date(gpio):
    now = time.localtime()

    wiringpi.wiringPiI2CWrite(_gpio, _I2CFlush)

    now.tm_sec =  _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _SECOND_REGISTER))
    now.tm_min =  _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _MINUTE_REGISTER))

    if use12hour:
        now.tm_hour = _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _HOUR_REGISTER))
    if date.tm_hour > 12:
        now.tm_hour -= 12
    else:
        now.tm_hour = _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _HOUR_REGISTER))

    now.tm_wday = _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _WEEK_REGISTER))
    now.tm_mday = _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _DAY_REGISTER))
    now.tm_mon =  _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _MONTH_REGISTER))
    now.tm_year = _bcd_to_dec(wiringpi.wiringPiI2CReadReg8(gpio, _YEAR_REGISTER))
    now.tm_isdst = 0
    
    return time.mktime(now)

def display(tubes):
    def rev_bits(nval):
        reversed = 0

        i = 0
        while i < 64:
            if nval & 1 << i:
                reversed |= 1 << (63 - i)
  
        return reversed
    
    def list_to_bits(lst):
        bits = 0

        for n in range(8):
            bits |= lst[0]
            bits <<= 8

        return bits
            
    wiringpi.pinMode(_LE_PIN, _OUTPUT)
    wiringpi.digitalWrite(_LE_PIN, _LOW)

    display = tubes
    if _ncsHV5222:
        reverse = rev_bits(lst_to_bits(display))

        display[4] = reverse
        display[5] = reverse >> 8
        display[6] = reverse >> 16
        display[7] = reverse >> 24
        display[0] = reverse >> 32
        display[1] = reverse >> 40
        display[2] = reverse >> 48
        display[3] = reverse >> 56
  
    wiringpi.wiringPiSPIDataRW(0, display, 8)
    wiringpi.digitalWrite(_LE_PIN, _HIGH)

def update_backlight(color):
    wiringpi.softPwmWrite(_RED_LIGHT_PIN, color[0])
    wiringpi.softPwmWrite(_GREEN_LIGHT_PIN, color[1])
    wiringpi.softPwmWrite(_BLUE_LIGHT_PIN, color[2])

def ncs31x():
    wiringpi.wiringPiSetup()

    # wiringpi.softToneCreate(BUZZER_PIN)
    # wiringpi.softToneWrite(BUZZER_PIN, 1000)

    wiringpi.softPwmCreate(_RED_LIGHT_PIN, 0, MAX_POWER)
    wiringpi.softPwmCreate(_GREEN_LIGHT_PIN, 0, MAX_POWER)
    wiringpi.softPwmCreate(_BLUE_LIGHT_PIN, 0, MAX_POWER)

    if _conf_dict['backState']:
        update_backlight(conf_dict['backColor'])

    # open the I2C bus to the NCS31X device
    gpio = wiringpi.wiringPiI2CSetup(I2CAdress)
    if wiringpi.wiringPiSPISetupMode(0, 2000000, 2):
        return -1;

    # initialize the display
    wiringpi.pinMode(_R5222_PIN, _INPUT)
    wiringpi.pullUpDnControl(_R5222_PIN, _PUD_UP)

    _ncsHV5222 = not(wiringpi.digitalRead(_R5222_PIN))

    return gpio
