import os

import mutagen.id3
from mutagen.easyid3 import EasyID3


class MyLibrary(object):
    directories = ["/home/oddnaughty/Music/ytdl/", "/media/oddnaughty/Datas/Music"]

    def __init__(self):
        pass

    def get_songs(self):
        for dir in self.directories:
            for root, dirs, files in os.walk(dir):
                for filename in files:
                    if filename.lower().endswith('.mp3'):
                        filepath = os.path.join(root, filename)
                        yield filepath

    def get_tag(sell, song_path):
        try:
            file = EasyID3(song_path)
        except mutagen.id3.ID3NoHeaderError:
            file = mutagen.File(song_path, easy=True)
            file.add_tags()
        return

if __name__ == '__main__':
    library = MyLibrary()
    for song_path in library.get_songs():
        print (song_path)