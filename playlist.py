import os
import config
from request import Request

class Playlist():
    def __init__ (self):
        # all files that have been uploaded
        self.all_files  = []
        # files that are being played
        self.playlist   = []
        # current file index
        self.current    = 0

    def handle_web_request (self, msg):
        mtype = msg.get("type")

        if mtype == Request.ADD_FILE:
            self.load_files()

        if mtype == Request.ORDER:
            from_i      = msg.get("from")
            to_i        = msg.get("to")
            self.order_playlist(from_i, to_i)

        if mtype == Request.QUEUE_FILE:
            to_i        = msg.get("to")
            filename    = msg.get("file")
            self.queue_file(to_i, filename)

        if mtype == Request.REMOVE_FILE:
            filename    = msg.get("file")
            self.dequeue(filename)

    # load previously-uploaded presentations
    def load_files (self):
        path = config.SAVE_FOLDER
        self.playlist = []

        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                item = {"file" : f}
                self.all_files.append(f)

        print("loaded presentation files", self.all_files)

    def load_playlist (self):
        fd = open("playlist", "r")

        for line in fd:
            self.playlist.append({"file" : line[:-1]})

        fd.close()
        print("loaded playlist", self.playlist)

    def save_playlist (self):
        fd = open("playlist", "w")

        for i in self.playlist:
            fd.write(i.get("file"))
            fd.write('\n')

        fd.close()
        print("saved playlist", self.playlist)

    def order_playlist (self, from_i, to_i):
        if (from_i >= 0 and from_i < len(self.playlist) and 
                to_i >= 0 and to_i < len(self.playlist)):
            tmp = self.playlist.pop(from_i)
            self.playlist.insert(to_i, tmp)
            self.save_playlist()

    def queue_file (self, to_index, filename):
        if self.all_files.count(filename) == 0:
            return

        for item in self.playlist:
            if item.get("file") == filename:
                return

        if to_index >= 0 and to_index <= len(self.playlist):
            self.playlist.insert(to_index, {'file' : filename})
            self.save_playlist()

    def dequeue (self, filename):
        for item in self.playlist:
            if item.get("file") == filename:
                self.playlist.remove(item)
                break

        self.save_playlist()

