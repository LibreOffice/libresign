#
# purpose:
# Connect to SD remote server and control LibreOffice instance
# 

import request

def run():
    # TODO start libreoffice
    # TODO connect to sd remote server
    pass

def handle_web_request(msg):
    if request.ADD_FILE == msg.type:
        print("we gots a new file")

