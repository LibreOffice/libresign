from sys import stderr
import os, time, sys
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

    def close_file (self):
        if self.docu:
            self.docu.dispose()
            self.docu = None

    def transition_next (self):
        # TODO move to next slide
        pass

    def start (self):
        soffice = "soffice"
        pipename = "libresign"

        # TODO make sure the binary is correct etc
        args = ["/usr/bin/soffice", '--nologo', '--nodefault', '--accept=pipe,name=libbo;urp']
        pid = subprocess.Popen(args).pid

        print("started libo", pid)

        print("Connecting to LibreOffice")

        self.local_context = uno.getComponentContext()
        self.resolver = self.local_context.ServiceManager.createInstanceWithContext(
                 'com.sun.star.bridge.UnoUrlResolver', self.local_context)

        tries = 0

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

