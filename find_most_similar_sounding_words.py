import pykakasi
import json
from Levenshtein import distance

kks = pykakasi.kakasi()


def get_romaji(word):
    return kks.convert(word)[0]['kunrei']


data = json.load(open("./data/adverb_kana.json"))
ending = "り"
outer_dict = dict()
for w1, h1 in data.items():
    if h1[-1] == ending:
        if len(h1) == 4:
            r1 = get_romaji(h1)
            inner_dict = dict()
            for w2, h2 in data.items():
                if w1 != w2:
                    if h2[-1] == ending:
                        if len(h2) == 4:
                            r2 = get_romaji(h2)
                            dh = distance(h1, h2)
                            dr = distance(r1, r2)
                            # if dh < min(len(h1), len(h2)):
                            inner_dict[w2] = dr
            print(w1)
            sorted_dict = dict(sorted(inner_dict.items(), key=lambda x: x[1]))
            outer_dict[w1] = sorted_dict

print("OK")
