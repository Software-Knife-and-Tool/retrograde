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
 **  rpi.h: raspberry pi include file
 **
 **/
#if !defined(GRAFCH_RPI_H_)
#define GRAFCH_RPI_H_

#include <ctime>
#include <getopt.h>
#include <iostream>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include <vector>

namespace grafch {
namespace gpio {

#include <softPwm.h>
#include <softTone.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <wiringPiSPI.h>

} /* namespace gpio */
} /* namespace grafch */

#endif /* GRAFCH_RPI_H_ */
