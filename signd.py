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

    def network_found(self):
        # logging.info("network found")
        if not web.running:
            web.start(self, self.messages)
            self.locontrol.start_info_screen()
    
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

            try:
                msg = self.messages.get(True, 1)
                self.handle_web_request(msg)
            except queue.Empty:
                pass

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
        self.locontrol.handle_web_request(msg)
        self.playlist.handle_web_request(msg)

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

