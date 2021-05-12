/********
 **
 **  SPDX-License-Identifier: MIT
 **
 **  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
 **
 **/

/********
 **
 **  python.c: python ncs31x interface
 **
 **/

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "python.h"

#include <assert.h>
#include <getopt.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <stdbool.h>

#include "ncs31x.h"

namespace grafch {
namespace {
static int numargs = 0;

static PyObject* grafch_numargs(PyObject *self, PyObject *args) {
  (void)self;
  if(!PyArg_ParseTuple(args, ":numargs"))
    return NULL;
  return PyLong_FromLong(numargs);
}

static PyObject* grafch_time(PyObject *self, PyObject *args) {
  (void)self;
  if(!PyArg_ParseTuple(args, ":time"))
    return NULL;
  return NULL;
}

static PyObject* grafch_date(PyObject *self, PyObject *args) {
  (void)self;
  if(!PyArg_ParseTuple(args, ":date"))
    return NULL;
  return NULL;
}

static PyObject* grafch_blank(PyObject *self, PyObject *args) {
  (void)self;
  if(!PyArg_ParseTuple(args, ":blank"))
    return NULL;
  return NULL;
}

static PyObject* grafch_unblank(PyObject *self, PyObject *args) {
  (void)self;
  if(!PyArg_ParseTuple(args, ":unblank"))
    return NULL;
  return NULL;
}

static PyObject* grafch_return(PyObject *self, PyObject *args) {
  (void)self;
  if(!PyArg_ParseTuple(args, ":return"))
    return NULL;
  return NULL;
}

#if 0
{ "grafch": "time" }
{ "grafch": "date" }
{ "grafch": "blank" }
{ "grafch": "unblank" }
{ "grafch": "return" }
{ "grafch": { "delay": 500 } }
{ "grafch": { "tube": 0, "state": true } }
{ "grafch": { "digit": 5, "value": 5 } }
{ "grafch": { "rotor": [ { "grafch": "time" }, { "grafch": "return" } ] } }
#endif

static PyMethodDef GrafchMethods[] = {
    {"numargs", grafch_numargs, METH_VARARGS,
     "Return the number of arguments received by the process."},
    {"time", grafch_time, METH_VARARGS, "Time command."},
    {"time", grafch_date, METH_VARARGS, "Date command."},
    {"time", grafch_blank, METH_VARARGS, "Blank command."},
    {"time", grafch_unblank, METH_VARARGS, "Unblank command."},
    {"time", grafch_return, METH_VARARGS, "Return command."},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef GrafchModule = {
    PyModuleDef_HEAD_INIT, "grafch", NULL, -1, GrafchMethods,
    NULL, NULL, NULL, NULL
};

static PyObject* PyInit_grafch(void) {
  return PyModule_Create(&GrafchModule);
}
  
} /* anonymous namespace */

/** * python module **/
PyObject* Python::Module(const char* pyfn) {
  PyObject *pName, *pModule;

  Py_Initialize();
  PyObject* sysPath = PySys_GetObject("path");

  /* Error checking of pName left out */
  pName = PyUnicode_DecodeFSDefault(pyfn);

  PyList_Insert(sysPath, 0, PyUnicode_FromString("/opt/ntag2/"));

  pModule = PyImport_Import(pName);
  Py_DECREF(pName);

  if (pModule == NULL) {
    PyErr_Print();
    fprintf(stderr, "Failed to load \"%s\"\n", pyfn);
  }

  Py_INCREF(pModule);
  
  printf("loaded %s\n", PyModule_GetName(pModule));

  return pModule;
}

/** * python interface **/
PyObject* Python::Call(PyObject* pModule, const char* pyfn, int argc, char** argv) {
  PyObject *pFunc, *pArgs, *pValue;
  int i;

  assert(pModule);

  pValue = NULL;

  /* pFunc is a new reference */
  pFunc = PyObject_GetAttrString(pModule, pyfn);

  if (pFunc && PyCallable_Check(pFunc)) {
    pArgs = PyTuple_New(argc);
    for (i = 0; i < argc; ++i) {
      pValue = PyLong_FromLong(atoi(argv[i]));
      if (!pValue) {
        Py_DECREF(pArgs);
        Py_DECREF(pModule);
        fprintf(stderr, "Cannot convert argument\n");
        return NULL;
      }
      /* pValue reference stolen here: */
      PyTuple_SetItem(pArgs, i, pValue);
    }
    pValue = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);
    if (pValue != NULL) {
      // printf("Result of call: %ld\n", PyLong_AsLong(pValue));
      Py_DECREF(pValue);
    }
    else {
      Py_DECREF(pFunc);
      Py_DECREF(pModule);
      PyErr_Print();
      fprintf(stderr,"Call failed\n");
      return NULL;
    }
  }
  else {
    if (PyErr_Occurred())
      PyErr_Print();
    fprintf(stderr, "Cannot find function \"%s\"\n", pyfn);
  }
  
  Py_XDECREF(pFunc);
  Py_DECREF(pModule);

  return pValue;
}

Python::Python() {
  numargs = 3;

  PyObject* module_ = Python::Module(const_cast<const char*>("grafch"));
  PyImport_AppendInittab("grafch", &PyInit_grafch);
  (void)Python::Call(module_, const_cast<const char*>("conf"), 0, NULL);
}

} /* grafch namespace */
