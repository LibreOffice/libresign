#!/bin/bash

git clone https://github.com:rptr/irpjs.git
virtualenv -p python3 env
source env/bin/activate
pip3 install Flask python-libxdo gevent-websocket

