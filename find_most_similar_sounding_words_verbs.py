import pykakasi
import requests as requests
import json
from Levenshtein import distance
import os
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

kks = pykakasi.kakasi()

def get_romaji(word):
    return kks.convert(word)[0]['kunrei']


data = json.load(open("./data/adverb_kana.json"))

df_adverbs = pd.read_csv('./data/common_onoma.csv')

data = df_adverbs["word"]


ending = "り"
outer_dict = dict()

db_dict = dict()
count = 0
for w1 in data:

    dict_ = dict()

    if w1[-1] != ending:
        # if len(h1) == 4:

        r1 = get_romaji(w1)
        inner_dict = dict()
        for w2 in data:
            if w1 != w2:
                if w2[-1] != ending:
                    # if len(h2) == 4:
                    r2 = get_romaji(w2)
                    dh = distance(w1, w2)
                    dr = distance(r1, r2)
                    # if dh < min(len(h1), len(h2)):
                    inner_dict[w2] = dr
        print(w1)
        sorted_dict = dict(sorted(inner_dict.items(), key=lambda x: x[1]))
        outer_dict[w1] = sorted_dict

        dict_["category"] = "verb"
        dict_["question"] = "auto"
        dict_["answer"] = w1
        dict_["target"] = w1
        dict_["mca_list"] = list(sorted_dict.keys())[:10]

        db_dict[count] = dict_

        count += 1

with open(os.path.join('./data', 'onoma.json'), 'w') as fp:
    json.dump(db_dict, fp)
fp.close()
print("OK")
