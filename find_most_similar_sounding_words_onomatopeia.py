import pykakasi
import json
from Levenshtein import distance
import os
import pandas as pd

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

        dict_["category"] = "onoma"
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
