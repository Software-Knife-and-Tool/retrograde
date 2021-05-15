##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## gra-afch NCS31X driver
##
###########

import wiringpi
from datetime import date, datetime

# GPIO constants
_R5222_PIN = 22
_LE_PIN = 3

_DEBOUNCE_DELAY = 150
_TOTAL_DELAY = 17
_UP_BUTTON_PIN = 1
_DOWN_BUTTON_PIN = 4
_MODE_BUTTON_PIN = 5

_BUZZER_PIN = 0

_I2CAdress = 0x68
_I2CFlush = 0

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

_LEFT_REPR_START = 5
_LEFT_BUFFER_START = 0
_RIGHT_REPR_START = 2
_RIGHT_BUFFER_START = 4

_tube_map = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

_ncsHV5222 = False
_conf_dict = None
_gpio = None

def string_to_color(str):
    def ctoi(nib):
        nval = 0

        if nib >= '0' & nib <= '9':
            nval = nib - '0'
        elif nib >= 'a' & nib <= 'f':
            nval = nib - 'a' + 10;
        elif (nib >= 'A' & nib <= 'F'):
            nval = nib - 'A' + 10
        else:
            nval = -1
        return nval

    def channel(msn, lsn):
        m = ctoi(msn);
        l = ctoi(lsn);

        return (m < 0 | l < 0) if -1 else (m << 4) + l

    r = channel(str[0], str[1])
    g = channel(str[2], str[3])
    b = channel(str[4], str[5])

    return [r, g, b];

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

def display_host_date():
    date = datetime.now().strftime('%m%d%y')
    display(date)
    return date

def display_rtc_time():
    now = get_rtc_date()
    return now
#    if (cfg.useSystemRTC):
#      seconds = time(NULL)
#      timeinfo = localtime (&seconds)
#
#      date.tm_mday = timeinfo.tm_mday
#      date.tm_wday = timeinfo.tm_wday
#      date.tm_mon =  timeinfo.tm_mon + 1
#      date.tm_year = timeinfo.tm_year - 100
#
#      writeRTCDate(*timeinfo)
#    
#    # NOTE: RTC relies on Nixie to keep time (e.g. no NTP). 
#    date = getRTCDate()
#
#    const char* format = '%H%M%S'
#    strftime(displayCString, 8, format, &date)
#
#    Display(displayCString)
    
def bcd_to_dec(val):
    return (val / 16 * 10) + (val % 16)

def dec_to_bcd(val):
    return (val / 10 * 16) + (val % 10)

def scale_rgb(nval):
    return int(nval / 2.55)

def reverse_bits(nval):
    reversed = 0

    i = 0
    while i < 64:
        if nval & 1 << i:
            reversed |= 1 << (63 - i)
  
    return reversed

# numeric string to bits
def get_rep(str, start):
    bits = 0

    bits = (_tube_map[str[start] - 0x30]) << 20
    bits |= (_tube_map[str[start - 1] - 0x30]) << 10
    bits |= (_tube_map[str[start - 2] - 0x30])
  
    return bits

def fill_buffer(nval, buffer, start):
    buffer[start] = nval >> 24
    buffer[start + 1] = nval >> 16
    buffer[start + 2] = nval >> 8
    buffer[start + 3] = nval

    return buffer;

def init_pin(pin):
    wiringpi.pinMode(pin, INPUT)
    wiringpi.pullUpDnControl(pin, PUD_UP)

# we don't pay attention to the argument?
def update_backlight(color):
    r = color[0]
    g = color[1]
    b = color[2]
  
    wiringpi.softPwmWrite(_RED_LIGHT_PIN, scale_rgb(0xff))
    wiringpi.softPwmWrite(_GREEN_LIGHT_PIN, scale_rgb(0x40))
    wiringpi.softPwmWrite(_BLUE_LIGHT_PIN, scale_rgb(0x0))

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

def buttons():
    # auto pin = _MODE_BUTTON_PIN
    init_pin(_UP_BUTTON_PIN)
    init_pin(_DOWN_BUTTON_PIN)
    init_pin(_MODE_BUTTON_PIN)

#    wiringpi.wiringPiISR(_MODE_BUTTON_PIN, _INT_EDGE_RISING,
#                    static unsigned long debounce = 0
# 
#                    if ((wiringpi.millis() - debounce) > DEBOUNCE_DELAY):
#
#
#                    [&pin, mutex]() . void:
#                      if (mutex.try_lock()):
#                        pin = MODE_BUTTON_PIN
#                        mutex.unlock()
#                       else
#                        yield()
#                    )
#
#    wiringpi.wiringPiISR(UP_BUTTON_PIN, INT_EDGE_RISING,
#                    [&pin, mutex]() . void:
#                      pin = UP_BUTTON_PIN
#                      mutex.unlock()
#                    )
#
#    wiringpi.wiringPiISR(DOWN_BUTTON_PIN, INT_EDGE_RISING,
#                    [&pin, mutex]() . void:
#                      pin = DOWN_BUTTON_PIN
#                      mutex.unlock()
#                    )

# figure out a fixed-width binary
# date struct.
def get_rtc_date():
    date = datetime.now()

    # date = datetime.now().strftime('%m%d%y')
    
    wiringpi.wiringPiI2CWrite(_gpio, _I2CFlush)

    date.tm_sec =  bcdToDec(wiringpi.wiringPiI2CReadReg8(_gpio, _SECOND_REGISTER))
    date.tm_min =  bcdToDec(wiringpi.wiringPiI2CReadReg8(_gpio, _MINUTE_REGISTER))

    if use12hour:
        date.tm_hour = bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio, HOUR_REGISTER))
    if date.tm_hour > 12:
        date.tm_hour -= 12
    else:
        date.tm_hour = bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio, HOUR_REGISTER))

    date.tm_wday = bcd_to_dec(wiringpi.wiringPiI2CReadReg8(_gpio, WEEK_REGISTER))
    date.tm_mday = bcdToDec(wiringpi.wiringPiI2CReadReg8(_gpio, DAY_REGISTER))
    date.tm_mon =  bcdToDec(wiringpi.wiringPiI2CReadReg8(_gpio, MONTH_REGISTER))
    date.tm_year = bcdToDec(wiringpi.wiringPiI2CReadReg8(_gpio, YEAR_REGISTER))
    date.tm_isdst = 0
    
    return date

def updateRTCHour(tm date):
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, HOUR_REGISTER, decToBcd(date.tm_hour))
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def updateRTCMinute(tm date):
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, MINUTE_REGISTER, decToBcd(date.tm_min))
    wiringpi.wiringPiI2CWriteReg8(_gpio, HOUR_REGISTER, decToBcd(date.tm_hour))
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def resetRTCSecond():
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, SECOND_REGISTER, 0)
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def writeRTCDate(tm date):
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)
    wiringpi.wiringPiI2CWriteReg8(_gpio, SECOND_REGISTER, decToBcd(date.tm_sec))
    wiringpi.wiringPiI2CWriteReg8(_gpio, MINUTE_REGISTER, decToBcd(date.tm_min))
    wiringpi.wiringPiI2CWriteReg8(_gpio, HOUR_REGISTER, decToBcd(date.tm_hour))
    wiringpi.wiringPiI2CWriteReg8(_gpio, WEEK_REGISTER, decToBcd(date.tm_wday))
    wiringpi.wiringPiI2CWriteReg8(_gpio, DAY_REGISTER, decToBcd(date.tm_mday))
    wiringpi.wiringPiI2CWriteReg8(_gpio, MONTH_REGISTER, decToBcd(date.tm_mon))
    wiringpi.wiringPiI2CWriteReg8(_gpio, YEAR_REGISTER, decToBcd(date.tm_year))
    wiringpi.wiringPiI2CWrite(_gpio, I2CFlush)

def dot_blink():
    last_time_blink = wiringpi.millis()

    if ((wiringpi.millis() - last_time_blink) >= 1000):
        lastTimeBlink = wiringpi.millis()
        dot_state = !dot_state
  
def add_blink_to_rep(var):
    if dotState:
        var &=~ _LOWER_DOTS_MASK
        var &=~ _UPPER_DOTS_MASK
    else:
       var |= _LOWER_DOTS_MASK
       var |= _UPPER_DOTS_MASK
  
    return var

# flash with date
def flash_date(seconds):
    n = 0
    
    while n < seconds:
        NcsBlank(true)
        wiringpi.delay(500)
        NcsBlank(false)
        DisplayDate()
        wiringpi.delay(500)
        n++
        
    if cfg.backState:
        update_backlight(cfg.backColor)

# flash with time
def flash_time(seconds):
    n = 0
    
    while n < seconds:
        ncs_blank(true)
        wiringpi.delay(500)
        ncs_blank(false)
        display_time()
        wiringpi.delay(500)
        n++
        
    if cfg.backState
        initBacklight(cfg.backColor)

def display_string(str):
    wiringpi.pinMode(_LE_PIN, _OUTPUT)
    if cfg.dotState
      dot_blink()

    rep_bits = get_rep(const_cast<char*>(cstr), LEFT_REPR_START)
    rep_bits = add_blink_to_rep(rep_bits)

    display = None

    fill_buffer(rep_bits, display, _LEFT_BUFFER_START)

    rep_bits = get_rep(const_cast<char*>(cstr), RIGHT_REPR_START)
    rep_bits = add_blink_to_rep(rep_bits)

    fill_buffer(rep_bits, display, _RIGHT_BUFFER_START)

    wiringpi.digitalWrite(_LE_PIN, _LOW)

    if _ncsHV5222:
        reverse = reverse_bits(*(uint64_t*)display)

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

def display_date():
  char displayCString[8]

  auto now = time(NULL)
  auto date = localtime(&now)

  const char* format = '%m%d%y'
  strftime(displayCString, 8, format, date)
  
  Display(displayCString)

def display_time():
  char displayCString[8]

  date = get_rtc_date()
  seconds = time(NULL)

  tm* timeinfo = localtime (&seconds)

  # NOTE:  RTC relies on system to keep time (e.g. NTP assisted for accuracy).
  if (cfg.useSystemRTC):
    seconds = time(NULL)
    timeinfo = localtime (&seconds)

    date.tm_mday = timeinfo.tm_mday
    date.tm_wday = timeinfo.tm_wday
    date.tm_mon =  timeinfo.tm_mon + 1
    date.tm_year = timeinfo.tm_year - 100

    writeRTCDate(*timeinfo)
  
  # NOTE: RTC relies on Nixie to keep time (e.g. no NTP).
  date = getRTCDate()

  const char* format = '%H%M%S'
  strftime(displayCString, 8, format, &date)

  Display(displayCString)

def version():
    return '0.0.1'

def gra_afch():
    wiringpi.wiringPiSetup()

    # wiringpi.softToneCreate(BUZZER_PIN)
    # wiringpi.softToneWrite(BUZZER_PIN, 1000)

    wiringpi.softPwmCreate(_RED_LIGHT_PIN, 0, MAX_POWER)
    wiringpi.softPwmCreate(_GREEN_LIGHT_PIN, 0, MAX_POWER)
    wiringpi.softPwmCreate(_BLUE_LIGHT_PIN, 0, MAX_POWER)

    if _conf_dict['backState']:
        update_backlight(conf_dict['backColor'])

    buttons()
  
    # Open the NCS31X device
    _gpio = wiringpi.wiringPiI2CSetup(I2CAdress)
    if wiringpi.wiringPiSPISetupMode(0, 2000000, 2):
        exit(254)

    # initialize the display
    wiringpi.pinMode(_R5222_PIN, _INPUT)
    wiringpi.pullUpDnControl(_R5222_PIN, _PUD_UP)

    _ncsHV5222 = !wiringpi.digitalRead(_R5222_PIN)
