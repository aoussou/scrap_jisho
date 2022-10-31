import os
import requests
import pandas as pd

from pathlib import Path
###############################################################################
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


###############################################################################
root_dir = "./data/"
url_base = 'https://jisho.org/search/'

word = '郊外'

word_url =  url_base + word
page = requests.get(word_url)

with open("./data/test", 'wb+') as f:
    f.write(page.content)
