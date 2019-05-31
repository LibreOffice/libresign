#
# This is the control panel backend.
# Using the development web server now but Flask is 
# apparently compatible with most/all web servers
#

import threading, logging

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
    flaskapp.app.run(debug=True, use_reloader=False, threaded=True)
    logging.info("stopping web server")

def push_request (request):
    if msg_queue:
        msg_queue.put(request)

def get_playlist ():
    return signd.get_playlist()

