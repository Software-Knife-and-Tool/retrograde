#
# grafch-daemon makefile
#
CXXFLAGS += -Wno-unused-result -Wsign-compare -g -fdebug-prefix-map=/build/python3.7-DSh9dq/python3.7-3.7.3=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector -Wformat -Werror=format-security -DNDEBUG -g -fwrapv -O3 -Wall
LIBS = -lwiringPi -lpython3.7m -L/usr/lib/python3.7/config-3.7m-arm-linux-gnueabihf -L/usr/lib -lcrypt -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions
INCLUDES = -I. -I/usr/include/python3.7

SRCS =	\
    ../src/grafch/daemon.cpp	\
    ../src/grafch/python.cpp	\
    ../src/grafch/ncs31x.cpp

.PHONY: grafch-daemon

grafch-daemon: $(SRCS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SRCS) $(LIBS) -o grafch-daemon

clean:
	@rm -f grafch-daemon
