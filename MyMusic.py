import os, shutil, subprocess, sys
import mutagen, mutagen.id3
from mutagen.easyid3 import EasyID3
from youtube_dl import YoutubeDL

class MyMusic(object):
    """
    A class that can make me confortable with my music o/
    """

    def __init__(self, yt_path=os.path.join(os.environ["HOME"], "Music/ytdl")):
        """
        :param yt_path: The directory to store da shit bitch
        """
        self.old_tags = {}
        self.yt_path = yt_path
        self.genres = ["Hardtek", "Hardcore","Frenchcore", "Drum'n'Bass", "Psytrance", "Trap"]

    def song_to_directory(self, path, filename, album="", genres=[]):
        """
        Edit the mp3 file (filename) metadatas if needed and put it in path/Artist/{Album}/Title
        """
        datas = filename.split(' - ')
        try:
            file = EasyID3(os.path.join(path, filename))
        except mutagen.id3.ID3NoHeaderError:
            file = mutagen.File(os.path.join(path, filename), easy=True)
            file.add_tags()
        datas = {
            "title": file.get("title", []) or [(datas[2][:-4] if len(datas) > 2 else datas[1][:-4])],
            "artist": file.get("artist", []) or [(datas[1] if len(datas) > 2 else datas[0])],
            "tracknumber": file.get("tracknumber", []) or [(datas[0] if len(datas) > 2 else "")],
            "album": file.get("album", []) or [album],
            "genre": file.get("genre", []) or [";".join(list(map(str.capitalize, genres)))],
        }
        zap= input("Informations pour {}\nZapper [z]\n{} : ".format(filename, datas))
        if zap != "z":
            datas = self.get_input_attributes(datas)
        print (datas)
        for k in datas.keys():
            file[k] = datas[k]
            self.old_tags[k] = datas[k] or self.old_tags.get(k, [])
        file.save()
        directory = os.path.join(path, file["artist"][0], file["album"][0])
        os.makedirs(directory, exist_ok=True)
        shutil.move(os.path.join(path, filename), os.path.join(directory, file["title"][0] + ".mp3"))

    def get_input_attributes(self, datas):
        """
        Function asking the metadatas via command-line input"
        :param datas: Already filled datas dict
        :return: datas ^_^
        """
        for i in datas.keys():
            r = input('Please enter {}[{}/{}][type 1 to chose the second] : '.format(i, datas[i], self.old_tags.get(i, "")))
            if r:
                if r == "1":
                    datas[i] = self.old_tags.get(i, "")
                else:
                    datas[i] = [r]
        return datas

    def get_song_from_yt(self, url):
        """
        Download a song from youtube or soundcloud and put it in self.yt_path converted to mp3 with filled metadatas
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'nocheckcertificate': False,
            'noplaylist': True,
            'outtmpl': os.path.join(self.yt_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }
        with YoutubeDL(ydl_opts) as ydl:
            datas = ydl.extract_info(url)
            self.song_to_directory(self.yt_path, datas['title'] + ".mp3")
            return True

    def sort_directory(self, dir_path):
        """
        Given a dir_path directory, self.song_to_directory every file from this directory
        """
        for file in sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]):
            self.song_to_directory(dir_path, file)
