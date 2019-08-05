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
from sys import stderr
import os, time, sys, logging
import subprocess, base64

from PIL import Image

import uno
import unohelper

import IPython
IR = IPython.embed

from com.sun.star.beans import PropertyValue
from com.sun.star.beans.PropertyState import DIRECT_VALUE

# This class handles communication with the running LibreOffice instance
connection_url = 'uno:pipe,name=libbo;urp;StarOffice.ComponentContext'

# This class receives messages (IRP) from the UNOClient
class LiboListener ():
    def on_slideshow_started (self, num_slides, current_slide):
        pass

    def on_slideshow_ended (self):
        pass

    def on_slide_notes (self, slide_index, html):
        pass

    def on_slide_updated (self, slide_number):
        pass

    def on_slide_preview (self, slide_number, image):
        pass

    def focus_info_screen (self):
        pass

    def error_no_document (self):
        pass

# This class handles communication with the running LibreOffice instance
class UNOClient():
    def __init__(self, locontrol, ):
        self.locontrol  = locontrol
        self.connected  = False
        self.frame      = "MyFrame"
        self.docu       = None

        self.file_open          = False
        self.current_filename   = ""

    # TODO In the Impress Remote Protocol, when starting a presentation 
    #      we return (send to the client) all the slide thumbnails of 
    #      the presentation. These are showed in the remote app
    #      So this is needed to emulate/ mimic the remote
    def play_file (self, filename, looping):
        filename = os.path.realpath(filename)
        flags = 8
        self.docu = self.desktop.loadComponentFromURL("file://"+filename, self.frame, flags, ())

        # make sure the presentation runs properly
        self.docu.Presentation.IsAlwaysOnTop        = True
        self.docu.Presentation.IsEndless            = looping
        self.docu.Presentation.IsFullScreen         = True
        self.docu.Presentation.IsMouseVisible       = False
        self.docu.Presentation.IsTransitionOnClick  = False
        self.docu.Presentation.Pause                = 1

        pages = self.docu.DrawPages.ElementNames

        # set defaults per page
        for name in pages:
            page = self.docu.DrawPages.getByName(name)
            page.HighResDuration = 99999
            page.TransitionDuration = 99999
            page.TransitionType = 0

        logging.debug("play file %s" % filename)
        self.file_open = True
        self.current_filename = filename
        self.locontrol.focus_info_screen()

    def get_previews (self):
        previews = []

        if not self.get_document():
            return previews

        pages = self.docu.DrawPages.ElementNames

        for name in pages:
            page = self.docu.DrawPages.getByName(name)
            img = page.PreviewBitmap.value

            filt = self.context.ServiceManager.createInstanceWithContext("com.sun.star.drawing.GraphicExportFilter", self.context)
            filt.setSourceDocument(page)

            data = []
            # TODO the pixel width/height are inaccurate, the full-width
            #      image is created instead
            data.append(PropertyValue('PixelWidth', 0, '200', DIRECT_VALUE))
            data.append(PropertyValue('PixelHeight', 0, '120', DIRECT_VALUE))
            data.append(PropertyValue('ColorMode', 0, '0', DIRECT_VALUE))

            args = []
            args.append(PropertyValue("MediaType", 0, 'image/png', DIRECT_VALUE))
            args.append(PropertyValue("URL", 0, 'file:///tmp/preview.png', DIRECT_VALUE))
            args.append(PropertyValue("FilterData", 0, data, DIRECT_VALUE))

            filt.filter(args)

            f = open('/tmp/preview.png', 'rb')
            img = f.read()
            f.close()

            b64 = base64.b64encode(img)

            previews.append('data:image/png;base64,{}'.format(b64.decode()))

        return previews

    #
    def get_notes (self):
        notes = []

        if self.get_document():
            pages = self.docu.DrawPages.ElementNames
    
            for name in pages:
                page = self.docu.DrawPages.getByName(name)
                notes.append(self.get_page_notes(page))

        return notes

    def get_page_notes (self, page):
        notes_page = page.getNotesPage()
        count = notes_page.Count
        service = notes_page.getByIndex(1)
        return service.String

    # 
    def close_file (self):
        if self.docu:
            self.docu.dispose()
            self.docu = None

        logging.debug("close file")
        self.file_open = False

    #
    def is_file_open (self):
        return self.file_open

    def get_current_filename (self):
        return self.current_filename

    def get_document (self):
        self.docu = self.desktop.getCurrentComponent()

        # Presentation is not available unless we have loaded 
        # a presentation (i think)
        # Controller is not available unless we are in slideshow mode
        try:
            if (self.docu != None and
                self.docu.Presentation != None):
                return True
        except:
            return False 

        return False

    # 
    def transition_next (self):
        if not self.get_document():
            return

        if not self.docu.Presentation.isRunning():
            return

        index   = self.docu.Presentation.Controller.getCurrentSlideIndex()
        num     = self.docu.Presentation.Controller.getCount()

        # already at last page and we're not looping
        # TODO dunno if this is actually needed
        if index == num - 1 and not self.docu.Presentation.IsEndless:
            self.close_file()
            self.locontrol.on_slideshow_ended()
        else:
            self.docu.Presentation.Controller.gotoNextSlide()
            index = self.docu.Presentation.Controller.getCurrentSlideIndex()
            self.locontrol.on_slide_updated(index)

    #
    def transition_previous (self):
        if not self.get_document():
            return

        if not self.docu.Presentation.isRunning():
            return

        self.docu.Presentation.Controller.gotoPreviousSlide()
        index = self.docu.Presentation.Controller.getCurrentSlideIndex()
        self.locontrol.on_slide_updated(index)

    def goto_slide (self, number):
        if not self.get_document():
            return

        if not self.docu.Presentation.isRunning():
            return

        self.docu.Presentation.Controller.gotoSlideIndex(number)
        self.locontrol.on_slide_updated(number)

    def presentation_start (self):
        if not self.get_document():
            return

        # already running
        if self.docu.Presentation.isRunning():
            return

        self.docu.Presentation.start()
        pages = self.docu.DrawPages
        self.locontrol.on_slideshow_started(pages.Count, 0)

    def send_slide_info (self):
        previews = self.get_previews()
        notes = self.get_notes()

        # no document / no document.DrawPages
        if len(previews) == 0 or len(notes) == 0:
            self.locontrol.on_no_document()

        for c in range(len(previews)):
            self.locontrol.on_slide_preview(c, previews[c])
            self.locontrol.on_slide_notes(c, notes[c])

    def presentation_stop (self):
        if not self.get_document():
            return

        if not self.docu.Presentation.isRunning():
            return

        self.docu.Presentation.end()
        self.locontrol.on_slideshow_ended()

    def blank_screen (self):
        if not self.get_document():
            return

        if not self.docu.Presentation.isRunning():
            return

        self.docu.Presentation.Controller.blankScreen(0)
        # NOTE only sending to notify JS Remote of success
        self.locontrol.on_slide_updated(0)

    def resume (self):
        if not self.get_document():
            return

        if not self.docu.Presentation.isRunning():
            return

        self.docu.Presentation.Controller.resume()
        self.locontrol.on_slide_updated(0)

    # 
    def set_looping (self, looping):
        if not self.get_document():
            return

        self.docu.Presentation.IsEndless = looping

    # 
    def start (self, connect=False):
        soffice = "soffice"
        pipename = "libresign"

        # only connect, don't start libreoffice
        if not connect:
            # TODO make sure the binary is correct etc
            args = ["/usr/bin/soffice", '--nologo', '--norestore', '--nodefault', '--accept=pipe,name=libbo;urp']
            pid = subprocess.Popen(args).pid
            # TODO make sure it actually started! -- thought if it doesn't it will
            #      simply fail to connect which is OK
            print("started libo", pid)
    
        self.local_context = uno.getComponentContext()
        self.resolver = self.local_context.ServiceManager.createInstanceWithContext(
                 'com.sun.star.bridge.UnoUrlResolver', self.local_context)
        tries = 0

        print("Connecting to LibreOffice")

        while True:
            tries += 1

            # if tries == 100:
            #     print("can't connect to libreoffice")
            #     return 1

            try:
                sys.stdout.write(".")
                sys.stdout.flush()
                self.context = self.resolver.resolve(connection_url)
                break
            except:
                time.sleep(0.1)

        self.locontrol.focus_info_screen()

        self.smgr = self.context.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext('com.sun.star.frame.Desktop', self.context)

        if not self.desktop:
            raise (Exception, "UNO: failed to create desktop")

        print("Connected to LibreOffice")

        self.connected = True

        self.presentation_start()

    def stop (self):
        pass

