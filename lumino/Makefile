#
#
#
.PHONY: lint
SRCS = \
	app.py               \
	lumino/__init__.py   \
	gra_afch/rotor.py    \
	gra_afch/ncs31x.py   \
	gra_afch/__init__.py

lint:
	@for i in $(SRCS); do	\
	    pylint $$i;		\
	done			\

lint-summary:
	@make lint | grep code
