import pykakasi
import requests as requests
import json
from Levenshtein import distance
import os
import pandas as pd

def check_condition(jlpt,is_usually_hira):

    proceed = True
    if (jlpt == "N1" or jlpt == "N2") and proceed:
        pass
    else:
        proceed = False

    if (is_usually_hira) and proceed:
        pass
    else:
        proceed = False

    return proceed


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


directory = os.path.join("./data")
file_path = os.path.join(directory, "verbs_processed.csv")
df_data = pd.read_csv(file_path)

data_words = df_data["word"]
data_hiragana = df_data["hiragana"]
data_is_usually_hira = df_data["is_usually_kana"]
data_jlpt = df_data["jlpt"]



ending = "り"
outer_dict = dict()

db_dict = dict()
count = 0
for i, w1 in enumerate(data_words):

    jlpt_w1 = data_jlpt[i]
    hiragana_w1 = data_hiragana[i]
    is_usually_hira_w1 = data_is_usually_hira[i]

    proceed = check_condition(jlpt_w1, is_usually_hira_w1)



    dict_ = dict()

    if proceed:
        r1 = get_romaji(hiragana_w1)


        inner_dict = dict()
        for j, w2 in enumerate(data_words):
            if w1 != w2:

                jlpt_w2 = data_jlpt[j]
                hiragana_w2 = data_hiragana[j]
                is_usually_hira_w2 = data_is_usually_hira[j]
                proceed = check_condition(jlpt_w2, is_usually_hira_w2)

                if proceed:
                    # if len(h2) == 4:
                    r2 = get_romaji(w2)
                    dh = distance(w1, w2)
                    dr = distance(r1, r2)
                    # if dh < min(len(h1), len(h2)):
                    inner_dict[hiragana_w2] = dr

        print(w1)
        sorted_dict = dict(sorted(inner_dict.items(), key=lambda x: x[1]))
        outer_dict[w1] = sorted_dict

        dict_["category"] = "ひらがな動詞"
        dict_["question"] = "db_random"
        dict_["word"] = w1
        dict_["answer"] = hiragana_w1
        dict_["target"] = ""
        dict_["mca_list"] = list(sorted_dict.keys())[:10]

        db_dict[count] = dict_

        count += 1

with open(os.path.join('./data', 'kana_verbs.json'), 'w') as fp:
    json.dump(db_dict, fp)
fp.close()
print("OK")
