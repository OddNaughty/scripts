import os, shutil
from copy import deepcopy
from mutagen.easyid3 import EasyID3


class Tagging(object):

    def __init__(self):
        self.old_tags = {}
        pass

    def song_to_directory(self, path, filename, album="", genres=[]):
        datas = filename.split(' - ')
        file = EasyID3(os.path.join(path, filename))
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
        directory = os.path.join(path, file["artist"][0])
        os.makedirs(directory, exist_ok=True)
        shutil.move(os.path.join(path, filename), directory)

    def get_input_attributes(self, datas):
        for i in datas.keys():
            r = input('Please enter {}[{}/{}] : '.format(i, datas[i], self.old_tags.get(i, "")))
            if r:
                if r == "1":
                    datas[i] = self.old_tags.get(i, "")
                else:
                    datas[i] = [r]
        return datas
