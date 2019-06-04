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
   
    def check_interface (self, filepath):
        if not os.path.isfile(filepath):
            return False

        with open(filepath, 'r') as fd:
            state = fd.readline()

        return state.count('up') == 1

    def poll_network (self):
        state = False

        # NOTE again, linux only
        # NOTE permission issues potentially?

        if self.check_interface('/sys/class/net/eth0/operstate'):
            state = True

        if self.check_interface('/sys/class/net/enp0s25/operstate'):
            state = True

        return state

    def main(self):
        while self.running:
            if config.HTTP_CABLE_ONLY:
                if self.poll_network():
                    self.network_found()
            else:
                self.network_found()

            if not self.messages.empty():
                msg = self.messages.get()
                self.handle_web_request(msg)
    
            time.sleep(0.1)

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

