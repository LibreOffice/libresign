#
# purpose:
# Connect to SD remote server and control LibreOffice instance
# 

import time, logging

from request import Request
import infoscreen, config, web
import unoremote 
import config as Config

# temp
SLIDE_TIME = 2

class LibreOfficeController():
    def __init__ (self, signd):
        self.signd              = signd
        self.libo_running       = False
        self.info_showing       = True
        self.paused             = False
        # name of file currently playing
        self.current_filename   = ""

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

        if (self.client.connected and 
                not self.slideshow_running and
                not self.paused):
            filename = self.signd.playlist.get_current()

            if filename:
                filename = 'presentations/' + filename
                self.client.play_file(filename)
                self.current_filename = filename
        
            logging.debug("locontrol.py: try play file")

        if (self.slideshow_running and 
                secs > self.last_transition + SLIDE_TIME and
                not self.paused):
            self.client.transition_next()
            self.last_transition = secs

            logging.debug("locontrol.py: try transition slide")

    def on_slideshow_started (self):
        self.slideshow_running = True
        self.last_transition = time.time()
        # self.stop_info_screen()

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

    # trigger stopping and starting a presentation
    def reload_presentation (self):
        self.slideshow_running = False
        self.client.close_file()

    def resume (self):
        self.paused = False

    def pause (self):
        self.paused = True
        self.client.close_file()
        self.slideshow_running = False

    def handle_web_request(self, msg):
        mtype = msg.get('type')

        if Request.PLAY_FILE == mtype:
            filename = msg.get('file')

            if filename != self.current_filename:
                self.reload_presentation()

        if Request.PLAY == mtype:
            self.resume()

        if Request.PAUSE == mtype:
            self.pause()

