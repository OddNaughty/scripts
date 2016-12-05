import os
import shutil
import mutagen
import mutagen.id3
from prompt_toolkit import prompt
from mutagen.easyid3 import EasyID3
from youtube_dl import YoutubeDL
from pprint import pprint


class MyMusic(object):
    """
    A class that can make me confortable with my music o/
    """
    genres_file = "genres.txt"
    tmp_dir = '/tmp/'
    ytdl_opts = {
        'format': 'bestaudio/best',
        'nocheckcertificate': False,
        'noplaylist': True,
        'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }]
    }
    yt_path = os.path.join(os.environ["HOME"], "Music/ytdl")

    def __init__(self, yt_path=None):
        """
        :param yt_path: The directory to store songs
        """
        self.old_tags = {}
        self.yt_path = yt_path or self.yt_path
        self.genres = self.get_genres()

    def get_genres(self, file=None):
        """
        Get Music genres from self.genres_files or param file. Must be coma-separated values.
        :param file: The path of the file describing genres
        :return: List of genres
        """
        try:
            g = open(file or self.genres_file)
            genres = [ge.strip() for ge in g.read().split(",") if ge.strip()]
        except Exception as e:
            genres = []
        return genres

    def download_file(self, url):
        """
        Download a song from youtube or soundcloud and return the file path
        """
        with YoutubeDL(self.ytdl_opts) as ydl:
            datas = ydl.extract_info(url)
            return (datas['title'] + ".mp3")

    def download_playlist(self, url):
        """
        Download a song from youtube or soundcloud and return a list of filepaths
        """
        new_opts = self.ytdl_opts
        new_opts['noplaylist'] = False
        with YoutubeDL(new_opts) as ydl:
            datas = ydl.extract_info(url)
            songs = []
            for i, song in enumerate(datas['entries']):
                songs.append(song['title'] + ".mp3")
            return songs

    def tag_file(self, file_path, tags):
        """
        Tag file using mutagen id3 !
        :param file: The path of the file
        :param tags: A dictionnary containing what to tag on the file
        :return: True if succeed else False
        """
        try:
            file = EasyID3(file_path)
        except mutagen.id3.ID3NoHeaderError:
            file = mutagen.File(file_path, easy=True)
            file.add_tags()
        for tag in tags:
            file[tag] = tags[tag]
        file.save()

    def move_file(self, file_path, artist, title, new_file_path=None):
        """
        Simply move file to user directory with artist - title.mp3 as filename
        :param file_path: Origin file path
        :param new_file_path: where to be moved, else yt_path configured in init
        :return:
        """
        new_path = new_file_path or self.yt_path
        shutil.move(file_path, os.path.join(new_path, "{} - {}.mp3".format(artist, title)))

    # def

    def song_to_directory(self, path, filename, album="", genres=[], tracknumber=""):
        """
        Edit the mp3 file (filename) metadatas if needed and put it in path/Artist/{Album}/Title
        """
        datas = filename.split(' - ')
        if len(datas) < 2:
            datas = filename.split('-')
        try:
            file = EasyID3(os.path.join(path, filename))
        except mutagen.id3.ID3NoHeaderError:
            file = mutagen.File(os.path.join(path, filename), easy=True)
            file.add_tags()
        print(datas)
        try:
            datas = {
                "title": file.get("title", []) or [(datas[2][:-4] if len(datas) > 2 else datas[1][:-4])],
                "artist": file.get("artist", []) or [(datas[1] if len(datas) > 2 else datas[0])],
                "tracknumber": file.get("tracknumber", []) or [tracknumber] or [(datas[0] if len(datas) > 2 else "")],
                "album": file.get("album", []) or self.old_tags['album'] if 'album' in self.old_tags else [album],
                "genre": file.get("genre", []) or self.old_tags['genre'] if 'genre' in self.old_tags else [";".join(list(map(str.capitalize, genres)))],
            }
        except IndexError as e:
            datas = {
                "title": file.get("title", []) or [(datas[2][:-4] if len(datas) > 2 else datas[0][:-4])],
                "artist": file.get("artist", []) or [(datas[1] if len(datas) > 2 else "")],
                "tracknumber": file.get("tracknumber", []) or [tracknumber] or [(datas[0] if len(datas) > 2 else "")],
                "album": file.get("album", []) or self.old_tags['album'] if 'album' in self.old_tags else [album],
                "genre": file.get("genre", []) or self.old_tags['genre'] if 'genre' in self.old_tags else [";".join(list(map(str.capitalize, genres)))],
            }
        zap = prompt("Informations pour {}\nZapper [z]\n{} : ".format(filename, datas))
        if zap != "z":
            datas = self.get_input_attributes(datas)
        print(datas)
        for k in datas.keys():
            file[k] = datas[k]
            self.old_tags[k] = datas[k] or self.old_tags.get(k, [])
        file.save()
        shutil.move(os.path.join(path, filename), os.path.join(path, "{} - {}.mp3".format(file["artist"][0], file["title"][0])))

    def get_input_attributes(self, datas):
        """
        Function asking the metadatas via command-line input"
        :param datas: Already filled datas dict
        :return: datas ^_^
        """
        for i in datas.keys():
            if i == "genre":
                datas[i] = self.manage_genre()
            else:
                r = prompt('Please enter {}[{}/{}][type 1 to chose the second] : '.format(i, datas[i], self.old_tags.get(i, "")))
                if r:
                    if r == "1":
                        datas[i] = self.old_tags.get(i, "")
                    else:
                        datas[i] = [r]
        return datas

    def manage_genre(self):
            new = []
            print("Choose genre(s). If multiple, do ';' between choices. Type 'a' to add a new genre")
            for i, v in enumerate(self.genres):
                print("{} - {}".format(i, v))
            r = prompt("Choice(s): ").split(';')
            if r == ["a"]:
                self.genres.append(prompt("New genre: ").strip())
                return (self.manage_genre())
            else:
                try:
                    new = [";".join(map(lambda l: self.genres[int(l)], r))]
                except ValueError as e:
                    print("Please enter a number...")
                    return self.manage_genre()
                return new

    def sort_directory(self, dir_path):
        """
        Given a dir_path directory, self.song_to_directory every file from this directory
        """
        for file in sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]):
            self.song_to_directory(dir_path, file)


# TODO: Check for encoding shit :o.
# TODO: Put all genres in a associated file
# TODO: History ? Ahahaha
# TODO: Put all that shit in a db on Geraud's server to do auto-completion and everything :)
# TODO: Have a fucking cache !
