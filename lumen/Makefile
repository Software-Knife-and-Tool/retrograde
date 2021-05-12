#
# vortex instruments
#
.PHONY: dist clean release

dist:
	make -C dist

release:
	make -C release -f release.mk

install:
	make -C dist -f install.mk uninstall install

clean:
	make -C dist clean
	make -C release -f release.mk  clean
