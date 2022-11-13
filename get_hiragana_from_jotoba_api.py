import requests as requests
import pandas as pd

def get_kana(word):
    URL = "https://jotoba.de/api/search/words"

    headers = {
        'Accept': 'application/json',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'query': word,
        'language': 'English',
        'no_english': True,
    }

    response = requests.post(url=URL, headers=headers, json=json_data).json()

    words = response["words"]
    word0 = words[0]
    kana = word0["reading"]["kana"]

    return kana


df_adverbs = pd.read_csv('./data/adverbs.csv')

word_list = df_adverbs["word"]

hiragana_dict = dict()

for w in word_list:
    print(w)
    hiragana_dict[w] = get_kana(w)

import json
import os
with open(os.path.join('./data', 'adverb_kana.json'), 'w') as fp:
    json.dump(hiragana_dict, fp)
fp.close()

