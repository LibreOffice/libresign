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

