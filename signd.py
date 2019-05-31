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

import locontrol, web, config
from request import Request
 
class Sign():
    def __init__(self):
        self.running    = True
        self.messages   = queue.Queue()
        self.playlist   = []

    def network_found(self):
        # logging.info("network found")
        if not web.running:
            web.start(self, self.messages)
    
    def network_lost(self):
        # logging.info("network lost")
        web.stop()
    
    def main(self):
        while self.running:
            if config.HTTP_CABLE_ONLY:
                # TODO poll for ethernet connection
                pass
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

        self.load_playlist()

        locontrol.run()
        self.main()

    def handle_web_request(self, msg):
        locontrol.handle_web_request(msg)

        if msg.get("type") == Request.ADD_FILE:
            self.load_playlist()

        if msg.get("type") == Request.ORDER:
            pass
            # self.order_playlist()

    # presentation info for the front-end
    def get_playlist(self):
        return self.playlist

    # load previously-uploaded presentations
    def load_playlist(self):
        path = config.SAVE_FOLDER
        c = 1
        self.playlist = []

        # TODO store presentations.txt with FILENAME:FILE_ID

        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                item = {"file" : f, "file_id" : c}
                self.playlist.append(item)
                c += 1

        print("loaded playlist", self.playlist)

if __name__ == "__main__":
    sign = Sign()
    sign.setup()

