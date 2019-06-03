#

from enum import Enum

class Request(Enum):
    # choose a file to play
    PLAY_FILE       = 1
    # pause current file
    PAUSE           = 2
    # remove a file from playlist
    REMOVE_FILE     = 3
    # add file to playlist
    ADD_FILE        = 4
    # change order of files (item.pop(i), item.insert(j))
    ORDER           = 5
    # play/ unpause current file
    PLAY            = 6
    # move file from files list to playlist
    QUEUE_FILE      = 7

