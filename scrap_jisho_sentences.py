import copy

import pandas as pd
import os
from verb_inflections import get_forms
from jisho_api import get_jisho_data, get_sentences_page1
import json

root_dir = "./data/"
save_dir_jisho_sentences = os.path.join(root_dir, "sentences")
save_dir_jisho_api_data = os.path.join(root_dir, "api_data")

directory = os.path.join("./data")

type = "verbs"
# file_path = os.path.join(directory, "i_adjs_processed.csv")
# is_adj = True


file_path = os.path.join(directory, type  + "_processed.csv")
is_verb = True
is_adj = False

df_data = pd.read_csv(file_path)

data_words = df_data["word"]
data_hiragana = df_data["hiragana"]
data_is_usually_hira = df_data["is_usually_kana"]
data_jlpt = df_data["jlpt"]

sentences_dict = dict()

db_dict = dict()

# forms = get_forms("まく", False)
# print(forms)
# STOP


for i, word in enumerate(data_words):

    # if data_is_usually_hira[i]:

        reading = data_hiragana[i]
        jisho_data_path = os.path.join(save_dir_jisho_api_data, word) + ".json"



        jisho_data = get_jisho_data(word, reading, jisho_data_path)

        if is_verb:
            kanji_forms = get_forms(word, jisho_data["is_ichidan"])
            kana_forms = get_forms(reading, jisho_data["is_ichidan"])
        else:
            kana_forms = None


        if is_adj:
            reading = reading[:-1]

        path = os.path.join(save_dir_jisho_sentences, word)
        sentence_list, english_list, form_list = get_sentences_page1(
            word,
            reading=reading,
            kana_forms=kana_forms,
            path=path
        )

        if not sentence_list:
            path = os.path.join(save_dir_jisho_sentences, reading)
            sentence_list, english_list, form_list = get_sentences_page1(reading, reading=reading, kana_forms=kana_forms, path=path)

        word_dict = copy.copy(jisho_data)

        is_kana_list = []

        for s_nbr, form in enumerate(form_list):
            if kanji_forms[form] in sentence_list[s_nbr]:
                is_kana_list.append(0)
            else:
                is_kana_list.append(1)

        word_dict["japanese_sentences"] = sentence_list
        word_dict["english_sentences"] = english_list
        word_dict["verb_forms"] = form_list
        word_dict["is_usually_kana"] = int(data_is_usually_hira[i])
        word_dict["is_kana"] = is_kana_list
        word_dict["jlpt"] = data_jlpt[i]
        sentences_dict[word] = word_dict

with open(os.path.join('./data', type + '_sentences.json'), 'w') as fp:
    json.dump(sentences_dict, fp)
fp.close()
