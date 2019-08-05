#!/usr/bin/python3

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
# libreoffice sign main program
#
# intended purpose: 
#   start libo controller
#   detect network connection
#   start and stop web server
#   

import time, logging, signal, queue, os, sys, subprocess

import web, config
from playlist import Playlist
from request import Request
from locontrol import LibreOfficeController

sys.path.append('./irpjs')
import irp
 
class Sign():
    def __init__(self, irp_pid = 0):
        self.running    = True
        self.messages   = queue.Queue()
        self.playlist   = Playlist()
        self.locontrol  = LibreOfficeController(self)
        # the interface we are using
        self.net_iface = ""
        self.irp_server_process_id  = irp_pid

    def network_found(self):
        # logging.info("network found")
        if not web.running:
            web.start(self, self.messages)
            self.locontrol.start_info_screen()
            self.locontrol.start_libreoffice()
    
    def network_lost(self):
        # logging.info("network lost")
        web.stop()
        self.locontrol.stop_info_screen()
   
    def check_interface (self, path):
        # check if loopback (linux/include/linux/if_arp.h)
        with open(path+'/type', 'r') as fd:
            if int(fd.readline()) == 772:
                return False

        # TODO cable only? -- i think the purpose of the "cable only" idea
        #      was to make sure that the web control panel is only accessible
        #      when a person with physical access to the computer connects a
        #      cable

        with open(path+'/carrier', 'r') as fd:
            state = bool(int(fd.readline()))

        return state

    def poll_network (self):
        state = False

        for iface in os.listdir('/sys/class/net/'):
            if os.path.isdir('/sys/class/net/'+iface):
                state = self.check_interface('/sys/class/net/'+iface)
                if state:
                    self.net_iface = iface
                    break

        return state

    def main(self):
        while self.running:
            if config.HTTP_CABLE_ONLY:
                if self.poll_network():
                    self.network_found()
                else:
                    self.network_lost()
            else:
                # repeated invocations do nothing
                self.network_found()

            # get requests from web control panel, 0.2 second timeout
            try:
                msg = self.messages.get(True, 0.2)
                self.handle_web_request(msg)
            except queue.Empty:
                pass

            # if we're running with LIBO (debugging) or
            if not config.NO_LIBREOFFICE:
                self.locontrol.run_signage()

        self.network_lost()
   
    def setup(self):
        def sighand(signal, frame):
            self.running = False

        signal.signal(signal.SIGINT, sighand)
        logging.basicConfig(level=logging.DEBUG)

        self.playlist.load_files()
        self.playlist.load_playlist()

        self.main()

    def handle_web_request(self, msg):
        self.playlist.handle_web_request(msg)
        self.locontrol.handle_web_request(msg)

        logging.debug(msg)

    # playlist info for the front-end
    def get_playlist (self):
        return self.playlist

if __name__ == "__main__":
    for arg in sys.argv:
        # run only the web server (control panel) (debugging)
        if arg == '--onlyweb':
            config.NO_LIBREOFFICE = True
            config.SHOW_INFO_SCREEN = False

        # don't show the fullscreen info screen
        if arg == '--noinfo':
            config.SHOW_INFO_SCREEN = False

        # don't start libreoffice (debugging)
        if arg == '--nolibreoffice':
            config.NO_LIBREOFFICE = True

        # run as a digital sign
        if arg == '--sign':
            config.CONFERENCE = False

        # default anyway
        if arg == '--conference':
            config.CONFERENCE = True

        if arg == '--noremote':
            config.JS_REMOTE = False

    # start JS Remote server
    args = ['python3', 'irpjs/irp.py']
    irp_pid = subprocess.Popen(args).pid

    sign = Sign()
    sign.setup()

