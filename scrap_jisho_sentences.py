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
file_path = os.path.join(directory, "verbs_processed.csv")
df_data = pd.read_csv(file_path)

data_words = df_data["word"]
data_hiragana = df_data["hiragana"]
data_is_usually_hira = df_data["is_usually_kana"]
data_jlpt = df_data["jlpt"]

sentences_dict = dict()

for i, word in enumerate(data_words):

    if data_is_usually_hira[i]:

        reading = data_hiragana[i]
        jisho_data_path = os.path.join(save_dir_jisho_api_data,word) + ".json"

        print(word,reading)

        jisho_data = get_jisho_data(word, reading, jisho_data_path)

        forms = get_forms(reading, jisho_data["is_ichidan"])

        path = os.path.join(save_dir_jisho_sentences, word)
        sentence_list, english_list, form_list = get_sentences_page1(word, forms, path)

        if not sentence_list:
            path = os.path.join(save_dir_jisho_sentences, reading)
            sentence_list, english_list, form_list = get_sentences_page1(reading, forms, path)

        word_dict = copy.copy(jisho_data)

        word_dict["japanese_sentences"] = sentence_list
        word_dict["english_sentences"] = english_list
        word_dict["verb_forms"] = form_list

        sentences_dict[word] = word_dict


with open(os.path.join('./data', 'hiragana_verbs_sentences.json'), 'w') as fp:
    json.dump(sentences_dict, fp)
fp.close()

