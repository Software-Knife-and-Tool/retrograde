#
# vortex makefile
#
CC       = gcc
CXX	 = g++

CFLAGS   = -Wall -Wpedantic -Wextra -g
CXXFLAGS = -Wall -Wpedantic -Wextra -std=c++14 -g

.PHONY: dist clean

dist:
	@make CXX="$(CXX)" CXXFLAGS="$(CXXFLAGS)" -f grafch.mk

clean:
	@make -f grafch.mk clean
