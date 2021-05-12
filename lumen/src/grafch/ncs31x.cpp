/********
 **
 **  SPDX-License-Identifier: MIT
 **
 **  Copyright (c) 2017-2021 James M. Putnam <putnamjm.design@gmail.com>
 **  //============================================================================
 **  // Name        : DisplayNixie.cpp
 **  // Author      : GRA&AFCH @ Leon Shaner
 **  // Version     : v2.3.1
 **  // Copyright   : Free
 **  // Description : Display time on shields NCS314 v2.x or NCS312
 **  //============================================================================
 **
 **/

/********
 **
 **  ncs31x.cpp: NCS31x board
 **
 **/
#include "ncs31x.h"

#include <csignal>
#include <ctime>
#include <functional>
#include <iostream>
#include <mutex>
#include <thread>
#include <utility>
#include <vector>

#include <getopt.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

#include "python.h"

namespace grafch {
namespace {
  
const std::vector<uint16_t> TubeMap = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512};

int bcdToDec(int val) {
  return ((val / 16 * 10) + (val % 16));
}

int decToBcd(int val) {
  return ((val / 10 * 16) + (val % 10));
}

#if 0
tm addHourToDate(tm date) {
  date.tm_hour += 1;
  mktime(&date);
  return date;
}

tm addMinuteToDate(tm date) {
  date.tm_min += 1;
  mktime(&date);
  return date;
}
#endif

uint8_t scale_rgb(uint8_t src) {
  return int(float(src) / 2.55);
}

uint64_t reverseBit(uint64_t num) {
  uint64_t reverse_num = 0;

  for (auto i = 0; i < 64; i++) {
    if ((num & ((uint64_t)1<<i)))
      reverse_num = reverse_num | ((uint64_t)1 << (63 - i));
  }

  return reverse_num;
}

/** * numeric string to bits **/
uint32_t get32Rep(char* displayCString, int start) {
  uint32_t bits = 0;

  bits = (TubeMap[displayCString[start] - 0x30]) << 20;
  bits |= (TubeMap[displayCString[start - 1] - 0x30]) << 10;
  bits |= (TubeMap[displayCString[start - 2] - 0x30]);
  
  return bits;
}

void fillBuffer(uint32_t var32, unsigned char * buffer, int start) {
  buffer[start] = var32 >> 24;
  buffer[start + 1] = var32 >> 16;
  buffer[start + 2] = var32 >> 8;
  buffer[start + 3] = var32;
}

} /* namespace anonymous */

void Ncs31x::initPin(int pin) {
  gpio::pinMode(pin, INPUT);
  gpio::pullUpDnControl(pin, PUD_UP);
}

void Ncs31x::initBacklight(Daemon::Color color) {
  uint8_t r, g, b;
  
  std::tie(r, g, b) = color;
  gpio::softPwmWrite(Ncs31x::RED_LIGHT_PIN, scale_rgb(0xff));
  gpio::softPwmWrite(Ncs31x::GREEN_LIGHT_PIN, scale_rgb(0x40));
  gpio::softPwmWrite(Ncs31x::BLUE_LIGHT_PIN, scale_rgb(0x0));
}

#if 0
void funcMode(void) {
  static unsigned long debounce = 0;

  if ((gpio::millis() - debounce) > Ncs31x::DEBOUNCE_DELAY) {
    printf("MODE button was pressed.");
    debounce = gpio::millis();
  }
}

void funcUp(void) {
  static unsigned long debounce = 0;
  
  if ((gpio::millis() - debounce) > Ncs31x::DEBOUNCE_DELAY) {
    printf("UP button was pressed.");
    debounce = gpio::millis();
  }
}

void funcDown(void) {
  static unsigned long debounce = 0;
  
  if ((gpio::millis() - debounce) > Ncs31x::DEBOUNCE_DELAY) {
    printf("DOWN button was pressed.");
    debounce = gpio::millis();
  }
}
#endif

void Ncs31x::buttons() {
  // auto pin = Ncs31x::MODE_BUTTON_PIN;
  auto mutex = new std::mutex;

  auto button_thread =
    [mutex]() {
      // for (;;) {
        if (mutex->try_lock()) {
          mutex->unlock();
        } else
          std::this_thread::yield();
        // }
    };
  
  initPin(Ncs31x::UP_BUTTON_PIN);
  initPin(Ncs31x::DOWN_BUTTON_PIN);
  initPin(Ncs31x::MODE_BUTTON_PIN);

  // lock_entry_mutex();
  std::thread button_events(button_thread);
  button_events.detach();
  
#if 0
  gpio::wiringPiISR(MODE_BUTTON_PIN, INT_EDGE_RISING,
                    /** * debounce here **/
                    static unsigned long debounce = 0;
 
                    if ((gpio::millis() - debounce) > DEBOUNCE_DELAY) {

                    [&pin, mutex]() -> void {
                      if (mutex->try_lock()) {
                        pin = MODE_BUTTON_PIN;
                        mutex->unlock();
                      } else
                        yield();
                    });

  gpio::wiringPiISR(UP_BUTTON_PIN, INT_EDGE_RISING,
                    [&pin, mutex]() -> void {
                      pin = UP_BUTTON_PIN;
                      mutex->unlock();
                    });

  gpio::wiringPiISR(DOWN_BUTTON_PIN, INT_EDGE_RISING,
                    [&pin, mutex]() -> void {
                      pin = DOWN_BUTTON_PIN;
                      mutex->unlock();
                    });
#endif
}
    
tm Ncs31x::getRTCDate() {
  tm date;
    
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);

  date.tm_sec =  bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, SECOND_REGISTER));
  date.tm_min =  bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, MINUTE_REGISTER));

  if (use12hour) {
    date.tm_hour = bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, HOUR_REGISTER));
    if (date.tm_hour > 12)
      date.tm_hour -= 12;
  } else
    date.tm_hour = bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, HOUR_REGISTER));

  date.tm_wday = bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, WEEK_REGISTER));
  date.tm_mday = bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, DAY_REGISTER));
  date.tm_mon =  bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, MONTH_REGISTER));
  date.tm_year = bcdToDec(gpio::wiringPiI2CReadReg8(gpioFd, YEAR_REGISTER));
  date.tm_isdst = 0;
  return date;
}

void Ncs31x::updateRTCHour(tm date) {
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
  gpio::wiringPiI2CWriteReg8(gpioFd, HOUR_REGISTER, decToBcd(date.tm_hour));
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
}

void Ncs31x::updateRTCMinute(tm date) {
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
  gpio::wiringPiI2CWriteReg8(gpioFd, MINUTE_REGISTER, decToBcd(date.tm_min));
  gpio::wiringPiI2CWriteReg8(gpioFd, HOUR_REGISTER, decToBcd(date.tm_hour));
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
}

void Ncs31x::resetRTCSecond() {
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
  gpio::wiringPiI2CWriteReg8(gpioFd, SECOND_REGISTER, 0);
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
}

void Ncs31x::writeRTCDate(tm date) {
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
  gpio::wiringPiI2CWriteReg8(gpioFd, SECOND_REGISTER, decToBcd(date.tm_sec));
  gpio::wiringPiI2CWriteReg8(gpioFd, MINUTE_REGISTER, decToBcd(date.tm_min));
  gpio::wiringPiI2CWriteReg8(gpioFd, HOUR_REGISTER, decToBcd(date.tm_hour));
  gpio::wiringPiI2CWriteReg8(gpioFd, WEEK_REGISTER, decToBcd(date.tm_wday));
  gpio::wiringPiI2CWriteReg8(gpioFd, DAY_REGISTER, decToBcd(date.tm_mday));
  gpio::wiringPiI2CWriteReg8(gpioFd, MONTH_REGISTER, decToBcd(date.tm_mon));
  gpio::wiringPiI2CWriteReg8(gpioFd, YEAR_REGISTER, decToBcd(date.tm_year));
  gpio::wiringPiI2CWrite(gpioFd, I2CFlush);
}

void Ncs31x::dotBlink() {
  static unsigned int lastTimeBlink = gpio::millis();

  if ((gpio::millis() - lastTimeBlink) >= 1000) {
    lastTimeBlink=gpio::millis();
    dotState = !dotState;
  }
}

uint32_t Ncs31x::addBlinkTo32Rep(uint32_t var) {
  if (dotState) {
    var &=~LOWER_DOTS_MASK;
    var &=~UPPER_DOTS_MASK;
  } else {
    var |=LOWER_DOTS_MASK;
    var |=UPPER_DOTS_MASK;
  }

  return var;
}

void Ncs31x::NcsBlank(bool off) {
  if (off) {
    gpio::digitalWrite(grafch::Ncs31x::RED_LIGHT_PIN, LOW);
    gpio::digitalWrite(grafch::Ncs31x::GREEN_LIGHT_PIN, LOW);
    gpio::digitalWrite(grafch::Ncs31x::BLUE_LIGHT_PIN, LOW);
    gpio::digitalWrite(grafch::Ncs31x::LE_PIN, LOW);
    initBacklight(Daemon::Color{0, 0, 0});
  } else {   
    gpio::digitalWrite(grafch::Ncs31x::RED_LIGHT_PIN, HIGH);
    gpio::digitalWrite(grafch::Ncs31x::GREEN_LIGHT_PIN, HIGH);
    gpio::digitalWrite(grafch::Ncs31x::BLUE_LIGHT_PIN, HIGH);
    gpio::digitalWrite(grafch::Ncs31x::LE_PIN, HIGH);
  }
}                        

/** * flash with date **/
void Ncs31x::FlashDate(uint32_t seconds) {
  for (uint32_t n = 0; n < seconds; ++n) {
    NcsBlank(true);
    gpio::delay(500);
    NcsBlank(false);
    DisplayDate();
    gpio::delay(500);
  }
  
  if (cfg->backState)
    initBacklight(cfg->backColor);
}

/** * flash with time **/
void Ncs31x::FlashTime(uint32_t seconds) {
  for (uint32_t n = 0; n < seconds; ++n) {
    NcsBlank(true);
    gpio::delay(500);
    NcsBlank(false);
    DisplayTime();
    gpio::delay(500);
  }
  
  if (cfg->backState)
    initBacklight(cfg->backColor);
}

void Ncs31x::Display(const char cstr[8]) {
  gpio::pinMode(Ncs31x::LE_PIN, OUTPUT);
  if (cfg->dotState)
    dotBlink();

  uint32_t var32 = get32Rep(const_cast<char*>(cstr), Ncs31x::LEFT_REPR_START);
  var32 = addBlinkTo32Rep(var32);

  uint8_t display[8];
  
  fillBuffer(var32, display, LEFT_BUFFER_START);

  var32 = get32Rep(const_cast<char*>(cstr), Ncs31x::RIGHT_REPR_START);
  var32 = addBlinkTo32Rep(var32);

  fillBuffer(var32, display, RIGHT_BUFFER_START);

  gpio::digitalWrite(LE_PIN, LOW);

  if (Ncs31x::HV5222) {
    uint64_t reverse = reverseBit(*(uint64_t*)display);

    display[4] = reverse;
    display[5] = reverse >> 8;
    display[6] = reverse >> 16;
    display[7] = reverse >> 24;
    display[0] = reverse >> 32;
    display[1] = reverse >> 40;
    display[2] = reverse >> 48;
    display[3] = reverse >> 56;
  }

  gpio::wiringPiSPIDataRW(0, display, 8);
  gpio::digitalWrite(Ncs31x::LE_PIN, HIGH);
}

void Ncs31x::DisplayDate() {
  char displayCString[8];

  auto now = time(NULL);
  auto date = localtime(&now);

  const char* format = "%m%d%y";
  strftime(displayCString, 8, format, date);
  
  Display(displayCString);
}

void Ncs31x::DisplayTime() {
  char displayCString[8];

  tm date = getRTCDate();
  time_t seconds = time(NULL);
  tm* timeinfo = localtime (&seconds);

  // NOTE:  RTC relies on system to keep time (e.g. NTP assisted for accuracy).
  if (cfg->useSystemRTC) {
    seconds = time(NULL);
    timeinfo = localtime (&seconds);

    date.tm_mday = timeinfo->tm_mday;
    date.tm_wday = timeinfo->tm_wday;
    date.tm_mon =  timeinfo->tm_mon + 1;
    date.tm_year = timeinfo->tm_year - 100;

    writeRTCDate(*timeinfo);
  }

  /* NOTE: RTC relies on Nixie to keep time (e.g. no NTP). */
  date = getRTCDate();

  const char* format = "%H%M%S";
  strftime(displayCString, 8, format, &date);

  Display(displayCString);
}

#if 0
 void Ncs31x::blank(void) {
  gpio::digitalWrite(ncs31x::Ncs31x::RED_LIGHT_PIN, LOW);
  gpio::digitalWrite(ncs31x::Ncs31x::GREEN_LIGHT_PIN, LOW);
  gpio::digitalWrite(ncs31x::Ncs31x::BLUE_LIGHT_PIN, LOW);
  gpio::digitalWrite(ncs31x::Ncs31x::LE_PIN, LOW);
  // initBacklight(Daemon::Color{0, 0, 0});
}
  
void Ncs31x::unblank(void) {
  gpio::digitalWrite(grafch::Ncs31x::RED_LIGHT_PIN, HIGH);
  gpio::digitalWrite(grafch::Ncs31x::GREEN_LIGHT_PIN, HIGH);
  gpio::digitalWrite(grafch::Ncs31x::BLUE_LIGHT_PIN, HIGH);
  gpio::digitalWrite(grafch::Ncs31x::LE_PIN, HIGH);
}

void Ncs31x::delay500(void) { }
void Ncs31x::date(void) { }
#endif
 
Ncs31x::Ncs31x(Daemon* root) : cfg(root->cfg_) {  

  Python* python = new Python();
  (void)python;
  
  gpio::wiringPiSetup();

  // gpio::softToneCreate(BUZZER_PIN);
  // gpio::softToneWrite(BUZZER_PIN, 1000);

  gpio::softPwmCreate(RED_LIGHT_PIN, 0, Ncs31x::MAX_POWER);
  gpio::softPwmCreate(GREEN_LIGHT_PIN, 0, Ncs31x::MAX_POWER);
  gpio::softPwmCreate(BLUE_LIGHT_PIN, 0, Ncs31x::MAX_POWER);

  if (cfg->backState)
    initBacklight(cfg->backColor);

  buttons();
  
  /* Open the NCS31X device */
  gpioFd = gpio::wiringPiI2CSetup(I2CAdress);
  (void)gpio::wiringPiI2CSetup(I2CAdress);
  if (!gpio::wiringPiSPISetupMode (0, 2000000, 2))
    exit(254);

  /* initialize the display */
  gpio::pinMode(Ncs31x::R5222_PIN, INPUT);
  gpio::pullUpDnControl(R5222_PIN, PUD_UP);

  HV5222 = !gpio::digitalRead(R5222_PIN);

  /* set up the rotor */
  nth_ = 0;
  
  seq_ = std::vector<std::function<void(Ncs31x*)>>{time_disp,
                                                   delay500,
                                                   delay500};

  rotor_ = std::thread(render, this);
  rotor_.detach();
}

} /* namespace grafch */
