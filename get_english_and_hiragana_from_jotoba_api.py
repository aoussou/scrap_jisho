import requests as requests
import pandas as pd
import json
import os

def get_explanation(word):
    URL = "https://jotoba.de/api/search/words"

    headers = {
        'Accept': 'application/json',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'query': word,
        'language': 'English',
        'no_english': False,
    }

    response = requests.post(url=URL, headers=headers, json=json_data).json()

    words = response["words"]
    word0 = words[0]
    senses = word0["senses"]
    explanations = []

    count = 0
    for s in senses:

        explanations.append('; '.join(s["glosses"]))

    return explanations

df_adverbs = pd.read_csv('./data/common_onoma.csv')

word_list = df_adverbs["word"]

explanation_dict = dict()

for w in word_list:

    explanation = get_explanation(w)
    explanation_dict[w] = {"english": explanation}
    print(w,explanation)

with open(os.path.join('./data', 'onoma_explanation.json'), 'w') as fp:
    json.dump(explanation_dict, fp)
fp.close()

