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
 **  daemon.h: daemon include file
 **
 **/
#if !defined(GRAFCH_DAEMON_H_)
#define GRAFCH_DAEMON_H_

#include <csignal>
#include <ctime>
#include <functional>
#include <iostream>
#include <mutex>
#include <thread>
#include <utility>
#include <vector>

#include <getopt.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

#include "python.h"

namespace grafch {

class Daemon {
 public:
  typedef std::tuple<uint8_t, uint8_t, uint8_t> Color;
  
  typedef struct config {
    config(bool dotState,
           bool backState,
           Color backColor,
           bool useSystemRTC,
           bool use12hour,
           bool useRepl,
	   bool debug,
           std::string path,
           std::string form)
      : dotState(dotState),
        backState(backState),
        backColor(backColor),
        useSystemRTC(useSystemRTC),
        use12hour(use12hour),
        useRepl(useRepl),
	debug(debug),
        path(path),
        form(form)
    {}
  
    ~config() {}
  
    bool dotState;
    bool backState;
    Color backColor;
    bool useSystemRTC;
    bool use12hour;
    bool useRepl;
    bool debug;
    std::string path;
    std::string form;
  } Config;

  static constexpr auto NCS31X_VERSION = "0.0.3";

 private:
  static Config* options(int, char*[]);
  
 public: /* object model */
  Config* cfg_;
  Python* python_;
  
  Daemon(int argc, char* argv[]) : cfg_(options(argc, argv)), python_(new Python()) { }

}; /* class Daemon */

} /* grafch namespace */

#endif /* GRAFCH_DAEMON_H_ */
