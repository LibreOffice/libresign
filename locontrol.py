#
# purpose:
# Connect to SD remote server and control LibreOffice instance
# 

import time

from request import Request
import infoscreen, config, web
import unoremote 
import config as Config

# temp
SLIDE_TIME = 2

class LibreOfficeController():
    def __init__ (self, signd):
        self.signd          = signd
        self.libo_running   = False
        self.info_showing   = True

        if not Config.NO_LIBREOFFICE:
            self.start_libo()
            self.client = unoremote.UNOClient(self)
            self.client.start()

        self.last_transition    = 0
        self.slideshow_running  = False

    def start_libo (self):
        pass

    def run (self):
        if Config.NO_LIBREOFFICE:
            return

        secs = time.time()

        if self.client.connected and not self.slideshow_running:
            filename = self.signd.playlist.get_current()

            if filename:
                filename = 'presentations/' + filename
                self.client.play_file(filename)
                self.slideshow_running = True

        if (self.slideshow_running and 
                secs > self.last_transition + SLIDE_TIME):
            self.client.transition_next()
            self.last_transition = secs

    def on_slideshow_ended (self):
        self.slideshow_running = False
        self.signd.playlist.next()

    def start_info_screen (self):
        if config.SHOW_INFO_SCREEN:
            self.info_showing = True
            addr = web.get_address()
            infoscreen.start_info(addr)

    def stop_info_screen (self):
        if config.SHOW_INFO_SCREEN:
            self.info_showing = False
            infoscreen.stop_info()

    # def handle_irp_message (self, msg):
    #     print("IRP", msg)
    #     if 'slideshow_started' == msg:
    #         self.last_transition    = time.time()
    #         self.slideshow_running  = True

    #     elif 'slideshow_finished' == msg:
    #         self.slideshow_running = False

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

