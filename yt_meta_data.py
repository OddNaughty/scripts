#!/usr/local/bin/python3
import os
from Tagging import Tagging

dir_path = "/home/odn/Bureau/NewSound"
mytag = Tagging()
for file in sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]):
    mytag.song_to_directory(dir_path, file)

