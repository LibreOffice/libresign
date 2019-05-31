#!/usr/bin/python3
#
# libreoffice sign main program
#
# intended purpose: 
#   start libo controller
#   detect network connection
#   start and stop web server
#   

import time, logging, signal, queue
import locontrol, web, config
 
class Sign():
    def __init__(self):
        self.running    = True
        self.messages   = queue.Queue()

    def network_found(self):
        # logging.info("network found")
        if not web.running:
            web.start(self.messages)
    
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

        locontrol.run()
        self.main()

    def handle_web_request(self, msg):
        print("got web request")

if __name__ == "__main__":
    sign = Sign()
    sign.setup()

