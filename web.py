# Version: MPL 1.1
#
# This file is part of the LibreOffice project.
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# Contributor(s):
# Rasmus P J <wasmus@zom.bi>
#
# This is the control panel backend.
# Using the development web server now but Flask is 
# apparently compatible with most/all web servers
#

import threading, logging, socket, subprocess, string

import request as requests
import flaskapp, config

# TODO wrap this up into a class

msg_queue   = None
running     = None
thread      = None
files       = []
signd       = None

def start(signd_, msgs):
    global msg_queue, running, thread, signd

    signd = signd_

    if not running:
        msg_queue = msgs
        running = True
        thread = threading.Thread(target=web_thread, args=())
        thread.setDaemon(True)
        thread.start()

def stop():
    # TODO use other server than werkzeug and deal with shutdown at that point
    pass

def web_thread():
    logging.info("starting web server")
    flaskapp.app.run(debug=True, use_reloader=False, threaded=True, port=config.HTTP_PORT, host="0.0.0.0")
    logging.info("stopping web server")

def push_request (request):
    if msg_queue:
        msg_queue.put(request)

def get_playlist ():
    playlist = signd.get_playlist()
    return playlist.playlist

def get_all_files ():
    playlist = signd.get_playlist()
    return playlist.all_files

def get_current_playlist_item ():
    playlist = signd.get_playlist()
    return playlist.get_current()

def get_addr_1 ():
    # NOTE linux only -- best i could do
    p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    # TODO might be errors?
    addr, err = p.communicate()
    p.wait()

    # output of hostname something like "b'123.0.0.123 \n"
    addr = ''.join([c for c in str(addr) if c.isdigit() or c == '.'])

    return addr

# this works on Arch Linux ARM
def get_addr_pi ():
    # NOTE linux only -- best i could do
    p = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
    result, err = p.communicate()
    p.wait()

    iface = signd.net_iface
    found_iface = False

    addr = ""

    # regex knowledge would be useful...
    for line in str(result).split('\\n'):
        if found_iface:
            if line.find('inet ') >= 0:
                parts = [part for part in line.split(' ') if part != '']
                addr = parts[1]
                break

        if line.find(iface) >= 0:
            found_iface = True

    logging.debug("web::get_addr_pi(): got addr " + addr)

    return addr

def get_address ():
    port = config.HTTP_PORT
    addr = get_addr_1()

    if len(addr) == 0:
        addr = get_addr_pi()

    return 'http://' + addr + ':' + str(port) + '/'
