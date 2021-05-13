#
# release makefile
#
DIST   = ../dist
SRC    = ../src
LUMEN  = ./lumen-0.0.2
GRAFCH = ./grafch-0.0.2

.PHONY: release clean lumen grafch

release: lumen grafch

lumen: 
	@install -d $(LUMEN)
	@install -d $(LUMEN)/opt/lumen
	@install -d $(LUMEN)/opt/lumen/css
	@install -d $(LUMEN)/opt/lumen/html
	@install -d $(LUMEN)/opt/lumen/js
	@install -d $(LUMEN)/opt/lumen/node-modules
	@install -m 755 ../src/lumen/index.js $(LUMEN)/opt/lumen
	@install -m 755 ../src/lumen/*.json $(LUMEN)/opt/lumen
	@install -m 755 ../src/lumen/css/* $(LUMEN)/opt/lumen/css
	@install -m 755 ../src/lumen/html/* $(LUMEN)/opt/lumen/html
	@install -m 755 ../src/lumen/js/* $(LUMEN)/opt/lumen/js
	@tar cfz $(LUMEN).tgz $(LUMEN)
	@rm -rf $(LUMEN)

grafch: 
	@install -d $(GRAFCH)
	@install -d $(GRAFCH)/opt/grafch
	@install -m 755 $(DIST)/grafch-daemon $(GRAFCH)/opt/grafch
	@install -m 755 $(DIST)/grafch/install.sh $(GRAFCH)
	@install -m 755 $(DIST)/grafch/grafch.service $(GRAFCH)
	@install -m 644 $(SRC)/grafch/__init__.py $(GRAFCH)
	@install -m 644 $(SRC)/grafch/grafch-daemon.conf $(GRAFCH)
	@tar cfz $(GRAFCH).tgz $(GRAFCH)
	@rm -rf $(GRAFCH)

clean:
	@rm -rf $(LUMEN) $(LUMEN).tgz $(GRAFCH) $(GRAFCH).tgz
