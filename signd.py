# Version: MPL 1.1/LGPL 2.1
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
# Alternatively, the contents of this file may be used under the terms of
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL or the LGPL.
#
#!/usr/bin/python3
#
# libreoffice sign main program
#
# intended purpose: 
#   start libo controller
#   detect network connection
#   start and stop web server
#   

import time, logging, signal, queue, os

import web, config
from playlist import Playlist
from request import Request
from locontrol import LibreOfficeController
 
class Sign():
    def __init__(self):
        self.running    = True
        self.messages   = queue.Queue()
        self.playlist   = Playlist()
        self.locontrol  = LibreOfficeController(self)
        # the interface we are using
        self.net_iiface = ""

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

            self.locontrol.run()

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
        return self.playlist.playlist

    # all files info for the front-end
    def get_all_files (self):
        return self.playlist.all_files

if __name__ == "__main__":
    sign = Sign()
    sign.setup()

