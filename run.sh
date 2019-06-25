#!/bin/bash

source env/bin/activate

libo=/media/compd/libreoffice
# export PYTHONPATH=$libo:$libo/instdir/program
export PYTHONPATH=$libo
export LD_LIBRARY_PATH=$libo
export UNO_PATH=$libo
export URE_BOOTSTRAP=$libo/fundamentalrc
./signd.py

