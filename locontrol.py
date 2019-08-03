# Version: MPL 1.1
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
# purpose:
# Connect to SD remote server and control LibreOffice instance
# 

import time, logging

from xdo import Xdo
xdo = Xdo()

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

        self.last_transition    = 0
        self.slideshow_running  = False

    def start_libreoffice (self):
        self.client = unoremote.UNOClient(self)

        if not Config.NO_LIBREOFFICE:
            self.client.start()

    def run_signage (self):
        secs = time.time()

        # no slideshow running, try to play a file
        if (self.client.connected and 
                not self.slideshow_running and
                not self.paused):
            self.try_play_file()

            if not config.CONFERENCE:
                self.client.presentation_start()

        # slideshow is up, transition
        if (self.slideshow_running and 
                secs > self.last_transition + SLIDE_TIME and
                not self.paused and
                not config.CONFERENCE):

            self.client.transition_next()
            self.last_transition = secs

            logging.debug("locontrol.py: try transition slide")

    def on_slideshow_started (self, num_slides, current_slide_index):
        self.slideshow_running = True
        self.last_transition = time.time()

    def on_slideshow_ended (self):
        self.slideshow_running = False
        self.signd.playlist.next()
        self.focus_info_screen()

    def on_preview (self, index, image):
        pass

    def on_slide_updated (self, index):
        pass

    def on_slide_notes (self, index, notes):
        pass

    def focus_info_screen (self):
        pass

    def start_info_screen (self):
        if config.SHOW_INFO_SCREEN:
            self.info_showing = True
            addr = web.get_address()
            infoscreen.start_info(addr)

    def stop_info_screen (self):
        if config.SHOW_INFO_SCREEN:
            self.info_showing = False
            infoscreen.stop_info()

    def try_play_file (self):
        filename    = self.signd.playlist.get_current()
        size        = self.signd.playlist.get_playlist_size()
        loop        = size == 1

        if filename and not self.client.is_file_open():
            filename = 'presentations/' + filename
            self.client.play_file(filename, loop)
            self.current_filename = filename
            logging.debug("locontrol.py: try play file")

    # trigger stopping and starting a presentation
    def reload_presentation (self):
        self.slideshow_running = False
        self.client.close_file()
        self.try_play_file()

    def resume (self):
        self.paused = False

    def pause (self):
        self.paused = True
        self.client.close_file()
        self.slideshow_running = False

    # set looping on/off
    def playlist_changed (self):
        size = self.signd.playlist.get_playlist_size()
        self.client.set_looping(size == 1)

        newfile = self.signd.playlist.get_current()
        oldfile = self.client.get_current_filename()

        if newfile != oldfile:
            self.client.close_file()
            self.try_play_file()

        logging.debug("locontrol.py::playlist_changed()")

    def handle_web_request(self, msg):
        mtype = msg.get('type')

        if Request.QUEUE_FILE == mtype or Request.REMOVE_FILE == mtype:
            self.playlist_changed()

        if Request.PLAY_FILE == mtype:
            filename = msg.get('file')

            if filename != self.current_filename:
                self.reload_presentation()

        if Request.PLAY == mtype:
            self.resume()

        if Request.PAUSE == mtype:
            self.pause()

