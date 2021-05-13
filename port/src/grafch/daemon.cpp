/********
 **
 **  SPDX-License-Identifier: MIT
 **
 **  Copyright (c) 2017-2021 James M. Putnam <putnamjm.design@gmail.com>
 **
 **/

/********
 **
 **  ncs31x.cpp: ncs31x main
 **
 **/
#include "daemon.h"
#include "ncs31x.h"
#include "rpi.h"
#include "timer.h"

#include <csignal>
#include <ctime>
#include <functional>
#include <iostream>
#include <mutex>
#include <thread>
#include <utility>
#include <vector>

#include <getopt.h>
#include <string.h>
#include <unistd.h>

#include "python.h"

namespace grafch {
namespace {

auto CStringToColor(const char* str) {

  auto ctoi =
    [](char nib) -> int {
      int val;
      
      if (nib >= '0' && nib <= '9')
        val = nib - '0';
      else if (nib >= 'a' && nib <= 'f')
        val = nib - 'a' + 10;
      else if (nib >= 'A' && nib <= 'F')
        val = nib - 'A' + 10;
      else
        val = -1;

      return val;
    };
    
  auto channel =
    [ctoi](char msn, char lsn) -> int {
      int m, l;

      m = ctoi(msn);
      l = ctoi(lsn);

      return (m < 0 || l < 0) ? -1 : (m << 4) + l;
    };

  int r, g, b;

  if (strlen(str) != 6)
    Daemon::Color{0, 0, 0};

  r = channel(str[0], str[1]);
  g = channel(str[2], str[3]);
  b = channel(str[4], str[5]);

  return
    (r < 0 || b < 0 || b < 0) ? Daemon::Color{0, 0, 0} : Daemon::Color{r, g, b};
}

} /* anonymous namespace */

auto Daemon::options(int argc, char* argv[]) -> struct config* {
  const char* tags = "hve:bBc:xdD21nNrl:";
  
  const struct option opts[] = {
     {"12hour",    no_argument,       0, '1'},
     {"24hour",    no_argument,       0, '2'},
     {"back",      no_argument,       0, 'b'},
     {"color",     required_argument, 0, 'c'},
     {"dots",      no_argument,       0, 'd'},
     {"eval",      required_argument, 0, 'e'},
     {"load",      required_argument, 0, 'l'},
     {"help",      no_argument,       0, 'h'},
     {"log",       no_argument,       0, 'x'},
     {"no-back",   no_argument,       0, 'B'},
     {"no-dots",   no_argument,       0, 'D'},
     {"no-ntp",    no_argument,       0, 'N'},
     {"ntp",       no_argument,       0, 'n'},
     {"repl",      no_argument,       0, 'r'},
     {"version",   no_argument,       0, 'v'},
     {0,0,0,0},
  };

  auto cfg = new Config(false, false, Color{0xff, 0x40, 0x00}, false, false, false, false, "", "");

  for (;;) {
    auto arg = getopt_long(argc, argv, tags, opts, nullptr);

    switch (arg) {
    case 'v':
      printf("ncs31x: v%s\n", NCS31X_VERSION);
      exit(0);
      break;
    case 'r':
      cfg->useRepl = true;
      break;
    case 'l':
      cfg->path = optarg;
      break;
    case 'e':
      cfg->form = optarg;
      break;
    case 'b':
    case 'B':
      cfg->backState = arg == 'b';
      break;
    case 'c':
      cfg->backColor = CStringToColor(optarg);
      break;
    case 'd':
    case 'D':
      cfg->dotState = arg == 'd';
      break;
    case '1':
    case '2':
      cfg->use12hour = arg == '1';
      break;
    case 'n':
    case 'N':
      cfg->useSystemRTC = arg == 'n';
      break;
    case 'h':
      printf("Usage: ncs31x [OPTION]\n"
             "Ncs31x clock daemon\n"
             "  -h, --help: print this message and exit\n"
             "  -v, --version: print version and exit\n"
             "  -b, --back: turn on backlight (default)\n"
             "  -B, --no-back: turn off backlight\n"
             "  -c, --color: backlight color rrggbb (default ff4000)\n"
             "  -d, --dots, -d: flash indicators (default)\n"
             "  -e, --eval, -e: eval expression\n"
             "  -l, --load, -l: load file\n"
             "  -D, --no-dots, -D: turn off indicators\n"
             "  -2, --24hour, -2: 24 hour display\n"
             "  -1, --12hour, -1: 12 hour display (default)\n"
             "  -n, --ntp, -n: use NTP to improve accuracy (default)\n"
             "  -N, --no-ntp, N: rely on NSC31x RTC\n"
             "  -r, --repl, -r: repl\n"
             );
      exit(0);
    case 'x':
      cfg->debug = true;
      break;
    case -1:
      return cfg;
    }
  }
}

} /* namespace grafch */

/** * entry point **/
int main(int argc, char* argv[]) {

  auto root = new grafch::Daemon(argc, argv);
  auto ncs31x = new grafch::Ncs31x(root);
  (void)ncs31x;

  auto signal_handler =
    [](int sig_received) -> void {
      grafch::Ncs31x::NcsBlank(true);
      exit(sig_received);
    };

  signal(SIGINT, signal_handler);
  signal(SIGQUIT, signal_handler);
  signal(SIGTERM, signal_handler);

  // ncs31x->FlashDate(3);
  // ncs31x->NcsBlank(false);

  // ncs31x->RotorThread()->join();
  while (true) {
    std::this_thread::yield();
  }
  return 0;
}
