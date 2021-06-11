#! /bin/bash
BASE=/opt/retrograde
BIN=$BASE/venv/bin
PACKAGES=$BASE/retro:$BASE/retro/modules:$BASE/venv/lib/python3.7/site-packages

env "PATH=$BIN" "PYTHONPATH=$PACKAGES" python3 app.py
