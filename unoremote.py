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

    def play_file (self, filename):
        filename = os.path.realpath(filename)
        flags = 0
        self.docu = self.desktop.loadComponentFromURL("file://"+filename, self.frame, flags, ())
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

        # already at last page
        if index == num - 1:
            self.close_file()
            self.locontrol.on_slideshow_ended()
        else:
            self.docu.Presentation.Controller.gotoNextSlide()

        logging.debug("transition")

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

