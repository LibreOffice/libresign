#

from enum import Enum

class Request(Enum):
    PLAY            = 1
    STOP            = 2
    REMOVE_FILE     = 3
    ADD_FILE        = 4
    ORDER           = 5

# in case we want to add some more bells and whistles
def create_request (request_type, filename):
    return (request_type, filename)

