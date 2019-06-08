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

    def handle_web_request(msg):
        pass
        # if Request.ADD_FILE == msg["type"]:
        #     print("we gots a new file")
    
        # PLAY_FILE
    
        # PLAY
    
        # PAUSE
    
        # TODO msg to libreoffice process etc
