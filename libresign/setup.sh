#!/bin/bash

mkdir presentations
touch playlist
git clone https://github.com/rptr/irpjs.git
virtualenv -p python3 env
source env/bin/activate
pip3 install Flask python-libxdo gevent-websocket

