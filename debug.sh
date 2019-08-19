#!/bin/bash

if [ ! -d "presentations" ]; then
    mkdir presentations
fi

if [ ! -d "env" ]; then
    virtualenv --system-site-packages -p python3 env
    source env/bin/activate
    pip3 install Flask python-libxdo gevent-websocket
fi

touch playlist

# run
libo=$1

if [ ${#1} -eq 0 ]; then 
    echo "./run.sh /path/to/libreoffice"
    echo "Trying /usr/lib/libreoffice..."
    libo="/usr/lib/libreoffice"
fi

source env/bin/activate

export PYTHONPATH=$libo:'./libresign'
export LD_LIBRARY_PATH=$libo
export UNO_PATH=$libo
export URE_BOOTSTRAP=$libo/fundamentalrc
python3 -c "import signd; signd.run_script()"

