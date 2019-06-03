import os
import config

class Playlist():
    def __init__ (self):
        # all files that have been uploaded
        self.all_files  = []
        # files that are being played
        self.playlist   = []
        # current file index
        self.current    = 0

    # load previously-uploaded presentations
    def load_files (self):
        path = config.SAVE_FOLDER
        self.playlist = []

        # TODO store presentations.txt with FILENAME:FILE_ID

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
        # TODO check if file exists
        # TODO check for duplicate

        if to_index >= 0 and to_index <= len(self.playlist):
            self.playlist.insert(to_index, {'file' : filename})
            self.save_playlist()
