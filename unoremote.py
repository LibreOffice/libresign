# Version: MPL 1.1/LGPL 2.1
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
# Alternatively, the contents of this file may be used under the terms of
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL or the LGPL.
#
from sys import stderr
import os, time, sys, logging
import subprocess

import uno
import unohelper

# import com.sun.star.frame.FrameSearchFlag

# This class handles communication with the running LibreOffice instance
connection_url = 'uno:pipe,name=libbo;urp;StarOffice.ComponentContext'

# This class handles communication with the running LibreOffice instance
class UNOClient():
    def __init__(self, locontrol):
        self.locontrol = locontrol
        self.connected = False
        self.frame = "MyFrame"
        self.docu = None

    def play_file (self, filename, looping):
        filename = os.path.realpath(filename)
        flags = 0
        self.docu = self.desktop.loadComponentFromURL("file://"+filename, self.frame, flags, ())

        # make sure the presentation runs properly
        self.docu.Presentation.IsAlwaysOnTop        = True
        self.docu.Presentation.IsEndless            = looping
        self.docu.Presentation.IsFullScreen         = True
        self.docu.Presentation.IsMouseVisible       = False
        self.docu.Presentation.IsTransitionOnClick  = False
        self.docu.Presentation.Pause                = 0

        pages = self.docu.DrawPages.ElementNames
        
        # set defaults per page
        for name in pages:
            page = self.docu.DrawPages.getByName(name)
            # page.HighResDuration = 1.0
            # page.TransitionDuration = 1.0
            page.TransitionType = 0

        self.docu.Presentation.start()
        self.locontrol.on_slideshow_started()
        logging.debug("play file %s" % filename)

    def close_file (self):
        if self.docu:
            self.docu.dispose()
            self.docu = None

        logging.debug("close file")

    def transition_next (self):
        # Presentation is not available unless we have loaded a presentation (i think)
        # Controller is not available unless we are in slideshow mode
        if self.docu == None or self.docu.Presentation == None or self.docu.Presentation.Controller == None:
            return

        index   = self.docu.Presentation.Controller.getCurrentSlideIndex()
        num     = self.docu.Presentation.Controller.getCount()

        # already at last page and we're not looping
        if index == num - 1 and not self.docu.Presentation.IsEndless:
            self.close_file()
            self.locontrol.on_slideshow_ended()
        else:
            self.docu.Presentation.Controller.gotoNextSlide()

        logging.debug("transition")

    def set_looping (self, looping):
        self.docu.Presentation.IsEndless = looping

    def start (self):
        soffice = "soffice"
        pipename = "libresign"

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

            if tries == 100:
                print("can't connect to libreoffice")
                return

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
        # flags = FrameSearchFlag.CREATE + FrameSearchFlag.ALL
        flags = 0

    def stop (self):
        pass

