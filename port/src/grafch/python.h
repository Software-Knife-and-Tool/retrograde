/********
 **
 **  SPDX-License-Identifier: MIT
 **
 **  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
 **
 **/

/********
 **
 **  python.h: python class
 **
 **/
#include <assert.h>
#include <getopt.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <stdbool.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#if !defined(GRAFCH_PYTHON_H_)
#define GRAFCH_PYTHON_H_

#include <ctime>
#include <iostream>
#include <thread>
#include <vector>

#include <getopt.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

namespace grafch {

class Python {

 private:
  PyObject* module_;
  
 public:
  static PyObject* Module(const char*);
  static PyObject* Call(PyObject*, const char*, int, char**);

  Python();
  
}; /* Python class */

} /* namespace grafch */

#endif /* GRAFCH_PYTHON_H_ */
