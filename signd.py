#
# libreoffice sign "daemon"
#
# intended purpose: 
#   start libo controller
#   detect network connection
#   start and stop web server
#   

import time
import locontrol

def network_found():
    # TODO start up web server
    pass

def network_lost():
    # TODO shut down web server
    pass

def detect_network():
    while 1:
        print "..."
        # TODO detect: polling. various specific ways to do it
        time.sleep(1)

def setup():
    # TODO start libreoffice
    # TODO start libo controller
    pass

setup()
detect_network()




