#
# purpose:
# Connect to SD remote server and control LibreOffice instance
# 

from request import Request
import infoscreen

class LibreOfficeController():
    def __init__ (self, signd):
        self.signd          = signd
        self.libo_running   = False
        self.info_showing   = True

    def start_info_screen (self):
        self.info_showing = True

    def stop_info_screen (self):
        self.info_showing = False

def run():
    # TODO start libreoffice
    # TODO connect to sd remote server
    pass

def handle_web_request(msg):
    pass
    # if Request.ADD_FILE == msg["type"]:
    #     print("we gots a new file")

    # PLAY_FILE

    # PLAY

    # PAUSE

    # TODO msg to libreoffice process etc

