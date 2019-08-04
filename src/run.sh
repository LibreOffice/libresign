#!/bin/bash

libo=$1

if [ ${#1} -eq 0 ]; then 
    echo "./run.sh /path/to/libreoffice"
    echo "Trying /usr/lib/libreoffice..."
    libo="/usr/lib/libreoffice"
fi

. env/bin/activate

export PYTHONPATH=$libo:/usr/lib/python3/dist-packages:/usr/lib/python3.7/site-packages
export LD_LIBRARY_PATH=$libo
export UNO_PATH=$libo
export URE_BOOTSTRAP=$libo/fundamentalrc
python3 signd.py $@

