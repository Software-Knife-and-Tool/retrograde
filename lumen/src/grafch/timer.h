/********
 **
 **  SPDX-License-Identifier: MIT
 **
 **  Copyright (c) 2017-2021 James M. Putnam <putnamjm.design@gmail.com>
 **
 **/

/********
 **
 **  timer.h: timer module
 **
 **/
#if !defined(GRAFCH_TIMER_H_)
#define GRAFCH_TIMER_H_

#include <chrono>
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

#include "module.h"

namespace grafch {

class Timer : public Module {
 private:
  uint32_t msec_;
  std::thread* thread_;
  void (*cb_)();
  
  static void OneShot(Timer* timer) {
    std::this_thread::sleep_for(std::chrono::milliseconds(timer->msec_));
    timer->cb_();
  }

 public:
  void Sync() {
    thread_ = new std::thread(OneShot, this);
    thread_->join();
  }

  void Async() {
    thread_ = new std::thread(OneShot, this);
  }

  void Events() { };
  
  Timer(uint32_t msec, void (*cb)()) {
    msec_ = msec;
    cb_ = cb;
  }
}; /* class Timer */

} /* grafch namespace */

#endif /* GRAFCH_TIMER_H_ */
