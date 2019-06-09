#
# purpose:
# Connect to SD remote server and control LibreOffice instance
# 

from request import Request
import infoscreen, config, web
import sdremote

class LibreOfficeController():
    def __init__ (self, signd):
        self.signd          = signd
        self.libo_running   = False
        self.info_showing   = True
        self.client         = sdremote.SDRemoteClient()
        self.client.start()
        # TODO start LibreOffice Impress -- for now i am starting it manually
        #      for better control

    def run (self):
        self.client.receive()

    def start_info_screen (self):
        if config.SHOW_INFO_SCREEN:
            self.info_showing = True
            addr = web.get_address()
            infoscreen.start_info(addr)

    def stop_info_screen (self):
        if config.SHOW_INFO_SCREEN:
            self.info_showing = False
            infoscreen.stop_info()

    def handle_web_request(self, msg):
        mtype = msg.get('type')

        if Request.PLAY_FILE == mtype:
            # TODO need to either restart libreoffice, supplying the correct file
            #      or add a way of changing the current file while libreoffice is 
            #      running
            pass

        if Request.PLAY == mtype:
            pass

        if Request.PAUSE == mtype:
            pass

