#!/bin/bash

home=$PWD
libo=/media/compd/libreoffice/instdir/program
export PYTHONPATH=$libo
# export LD_LIBRARY_PATH=LD_LIBRARY_PATH:$libo
cp unoremote.py $libo/
cd $libo
./python unoremote.py

# NOTE so, calling ./python $home/unoremote.py gives me missing shared objects
#      need to look into how exactly python looks for shared libraries 

