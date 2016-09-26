# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    wallpaper.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cwagner <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/01/13 11:55:04 by cwagner           #+#    #+#              #
#    Updated: 2016/05/09 12:02:45 by cwagner          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from requests import get
from bs4 import BeautifulSoup
from urllib import request
from re import findall, match
from filecmp import cmp
import os

def get_number_from_file(filepath):
    x = findall(r'img(\d+).jpg', filepath)
    if x:
        return int(x[0])
    return 0

directory = os.environ["HOME"] + "/bjrmdm/"

last_file = directory + max([i for i in os.listdir(directory)], key=get_number_from_file)
base_url = 'http://dites.bonjourmadame.fr/'
r = get(base_url)
soup = BeautifulSoup(r.text, "html.parser")
img_url = soup.find('div', attrs={"class": "photo post"}).find('img').attrs['src']
file_name = "{}img{}.jpg".format(directory, int(findall(r'img(\d+).jpg', last_file)[0]) + 1)
print(img_url, file_name)
request.urlretrieve(img_url, file_name)

print ("I'm finished and everything goes well")
