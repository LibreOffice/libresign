#

from enum import Enum

class Request(Enum):
    PLAY_FILE       = 1
    PAUSE           = 2
    REMOVE_FILE     = 3
    ADD_FILE        = 4
    ORDER           = 5
    PLAY            = 6

