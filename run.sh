#!/bin/bash

if [ ${#1} -eq 0 ]; then 
    echo "./run.sh /path/to/libreoffice"
    echo "Trying /usr/lib/libreoffice..."
    1="/usr/lib/libreoffice"
fi

libo=$1

source env/bin/activate

# export PYTHONPATH=$libo:$libo/instdir/program
export PYTHONPATH=$libo
export LD_LIBRARY_PATH=$libo
export UNO_PATH=$libo
export URE_BOOTSTRAP=$libo/fundamentalrc
./signd.py

