#
# Impress Remote Control protocol impl
#

import socket

class SDRemoteClient():
    def __init__(self):
        self.sock = None
        self.addr   = ('localhost', 1599)

    def start (self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)
        self.sock.setblocking(False)
        self.send("LO_SERVER_CLIENT_PAIR\nLibreSign2\n12345\n\n")

    def send (self, data):
        sent = self.sock.send(data.encode('utf-8'))
        print("sent", sent)

    def receive (self):
        try:
            data = self.sock.recv(4096)
            self.handle_message(data.decode('utf-8').split('\n'))
        except:
            pass

    def handle_message (self, data):
        print(data)
        msg = data[0]

        # we need to input our pin manually in libreoffice
        if 'LO_SERVER_VALIDATING_PIN' == msg:
            pass

        elif 'LO_SERVER_SERVER_PAIRED' == msg:
            # TODO compare server version?
            # NOTE/TODO this also contains slideshow_finished, slideshow_info
            pass

        elif 'slideshow_started' == msg:
            pass

        elif 'slideshow_finished' == msg:
            pass

        elif 'slide_updated' == msg:
            pass

        elif 'slideshow_info' == msg:
            pass

        # base64 preview image, ignore
        elif 'slide_preview' == msg:
            pass
        # slide notes, ignore
        elif 'slide_notes' == msg:
            pass

    def transition_next(self):
        pass

    def transition_previous(self):
        pass

    def goto_slide(self):
        pass

    def slide_number(self):
        pass

    def presentation_start(self):
        pass

    def presentation_stop(self):
        pass

    def presentation_resume(self):
        pass

    def presentation_blank_screen(self):
        pass
