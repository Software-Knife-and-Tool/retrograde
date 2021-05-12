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
 **  ncs31x.h: ncs31x include file
 **
 **/
#if !defined(GRAFCH_NCS31X_H_)
#define GRAFCH_NCS31X_H_

#include <ctime>
#include <iostream>
#include <thread>
#include <vector>

#include <getopt.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

#include "daemon.h"
#include "ncs31x.h"
#include "module.h"
#include "rpi.h"

namespace grafch {

class Ncs31x : public Module {

 private:
  static const auto R5222_PIN = 22;
  static const auto LE_PIN = 3;

  static const auto DEBOUNCE_DELAY = 150;
  static const auto TOTAL_DELAY = 17;
  static const auto UP_BUTTON_PIN = 1;
  static const auto DOWN_BUTTON_PIN = 4;
  static const auto MODE_BUTTON_PIN = 5;

  static const auto BUZZER_PIN = 0;

  static const auto I2CAdress = 0x68;
  static const auto I2CFlush = 0;

  static const auto SECOND_REGISTER = 0x0;
  static const auto MINUTE_REGISTER = 0x1;
  static const auto HOUR_REGISTER = 0x2;
  static const auto WEEK_REGISTER = 0x3;
  static const auto DAY_REGISTER = 0x4;
  static const auto MONTH_REGISTER = 0x5;
  static const auto YEAR_REGISTER = 0x6;

  static const auto RED_LIGHT_PIN = 28;
  static const auto GREEN_LIGHT_PIN = 27;
  static const auto BLUE_LIGHT_PIN = 29;
  static const auto MAX_POWER = 100;

  static const auto UPPER_DOTS_MASK = 0x80000000;
  static const auto LOWER_DOTS_MASK = 0x40000000;

  static const auto LEFT_REPR_START = 5;
  static const auto LEFT_BUFFER_START = 0;
  static const auto RIGHT_REPR_START = 2;
  static const auto RIGHT_BUFFER_START = 4;

 private:
  int gpioFd;

  bool HV5222;
  bool dotState = 0;
  bool use12hour = true;

  /** * RTC time/date **/
  void updateRTCHour(tm);
  void updateRTCMinute(tm);
  void resetRTCSecond();
  void writeRTCDate(tm);
  tm getRTCDate();

  /** * indicators **/
  void dotBlink();
  uint32_t addBlinkTo32Rep(uint32_t);

  void Events() { };
  static void buttons();
  
  Daemon::Config* cfg;

  typedef std::vector<std::function<void(Ncs31x*)>> rotor;

  static auto render(Ncs31x* np) {
    for (;;)
      for (auto fn : np->seq_) fn(np);
  };

  std::thread rotor_;
  rotor seq_;
  size_t nth_;
  
  static void blank(Ncs31x* np) {
    gpio::digitalWrite(RED_LIGHT_PIN, LOW);
    gpio::digitalWrite(GREEN_LIGHT_PIN, LOW);
    gpio::digitalWrite(BLUE_LIGHT_PIN, LOW);
    gpio::digitalWrite(LE_PIN, LOW);
    np->initBacklight(Daemon::Color{0, 0, 0});
  }
  
  static void unblank(Ncs31x*) {
    gpio::digitalWrite(RED_LIGHT_PIN, HIGH);
    gpio::digitalWrite(GREEN_LIGHT_PIN, HIGH);
    gpio::digitalWrite(BLUE_LIGHT_PIN, HIGH);
    gpio::digitalWrite(LE_PIN, HIGH);
  }

  static void delay500(Ncs31x*) { gpio::delay(500); }
  
  static void date_disp(Ncs31x* np) {
    char displayCString[8];

    auto now = time(NULL);
    auto date = localtime(&now);

    const char* format = "%m%d%y";
    strftime(displayCString, 8, format, date);
  
    np->Display(displayCString);
  }

  static void time_disp(Ncs31x* np) {
    char displayCString[8];

    tm date = np->getRTCDate();
    time_t seconds = time(NULL);
    tm* timeinfo = localtime (&seconds);

    // NOTE:  RTC relies on system to keep time (e.g. NTP assisted for accuracy).
    if (np->cfg->useSystemRTC) {
      seconds = time(NULL);
      timeinfo = localtime (&seconds);

      date.tm_mday = timeinfo->tm_mday;
      date.tm_wday = timeinfo->tm_wday;
      date.tm_mon =  timeinfo->tm_mon + 1;
      date.tm_year = timeinfo->tm_year - 100;

      np->writeRTCDate(*timeinfo);
    }

    /* NOTE: RTC relies on Nixie to keep time (e.g. no NTP). */
    date = np->getRTCDate();

    const char* format = "%H%M%S";
    strftime(displayCString, 8, format, &date);

    np->Display(displayCString);
  }
  
 public:
  static void initPin(int);
  static void initBacklight(Daemon::Color);

  void FlashTime(uint32_t);
  void FlashDate(uint32_t);
  void Display(const char[8]);
  void DisplayTime(void);
  void DisplayDate(void);

  static void NcsBlank(bool);
  static void NcsDisplay(std::string);
  void NcsBlink(uint32_t);

  std::thread* RotorThread() {
    return &rotor_;
  }
  
  Ncs31x(Daemon*);
  
}; /* ncs31x class */

} /* namespace grafch */

#endif /* GRAFCH_NCS31X_H_ */
