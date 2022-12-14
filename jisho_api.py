import requests
import re
import pandas as pd
import os
import json
import time
request_session = requests.Session()


hiragana = pd.read_csv("./data/kana_list.csv", header=None)
hiragana_char_list = list(hiragana.iloc[:, 0])

def get_jisho_api_response(word,path):

    if os.path.isfile(path):
        data = json.load(open(path))
    else:
        request_string = "https://jisho.org/api/v1/search/words?keyword={0}".format(word)
        res = requests.get(request_string)

        while res.status_code != 200:
            time.sleep(1)
            res = requests.get(request_string)

        text = json.loads(res.text)
        data = text["data"]

        with open(path, 'w') as fp:
            json.dump(data, fp)
        fp.close()

    return data




def get_jisho_data(word, reading, path):

    data = get_jisho_api_response(word, path)

    for word_data in data:

        if word_data["japanese"][0]["reading"] == reading:

            senses = word_data["senses"]
            explanations = ""

            count = 0
            for s in senses:
                count += 1
                explanations += str(count) + str(". ") + '; '.join(s["english_definitions"]) + "\n"

            if count == 1:
                explanations = explanations.replace(str(count) + str(". "), "")

            if explanations[-1] == "\n":
                explanations = explanations[:-1]



            dict_ = dict()

            dict_["word"] = word
            dict_["reading"] = reading
            dict_["explanations"] = explanations

            if senses[0]["parts_of_speech"]:
                if "Ichidan" in senses[0]["parts_of_speech"][0]:
                    dict_["is_ichidan"] = 1
                else:
                    dict_["is_ichidan"] = 0

            return dict_

def get_sentences_page1(word, reading = None, kana_forms=None, path="None"):

    english_identifier = """<span class="english">"""

    sentence_remove = [
        """      """,
        """\n""",
        """<li class="clearfix">""",
        """<span class="unlinked">""",
        """</span>""",
        """</li>""",
        """<span class="unlinked">""",
        english_identifier
    ]

    url = 'https://jisho.org/search/{0} %23sentences'.format(word)



    furigana = pd.read_csv("./data/kana_list.csv", header=None)
    hiragana_char_list = list(furigana.iloc[:, 0])

    furigana_span = """<span\s+class\="furigana">(?:(?!</span>)(?:.|\n))*</span>"""
    sentence_identifier = """<ul class="japanese_sentence japanese japanese_gothic clearfix" lang="ja">"""

    sentence_list = []
    english_list = []
    form_list = []

    if not os.path.isfile(path):
        page = request_session.get(url)
        lines = page.text.splitlines()

        sleep_time = 0
        while """<h1>We're sorry, but something went wrong.</h1>""" in lines[18] :
            sleep_time += 1
            time.sleep(sleep_time)
            page = request_session.get(url)
            lines = page.text.splitlines()
        sleep_time = 0

        with open(path, 'wb+') as f:
            f.write(page.content)

    else:
        with open(path) as f:
            lines = f.readlines()



    for i, l in enumerate(lines):
        # print(i)
        if sentence_identifier in l:

            sentence_line = lines[i + 1]
            kanji_sentence = re.sub(furigana_span, '', sentence_line)


            for exp in sentence_remove:
                kanji_sentence = kanji_sentence.replace(exp, "")

            hiragana_sentence = ""

            for c in sentence_line:
                if c in hiragana_char_list:
                    hiragana_sentence += c

        if english_identifier in l:
            english = l

            if kana_forms is not None:

                for form, inflected_verb in kana_forms.items():

                    if inflected_verb in hiragana_sentence:

                        for exp in sentence_remove:
                            english = english.replace(exp, "")

                        sentence_list.append(kanji_sentence)
                        english_list.append(english)
                        form_list.append(form)

                        break

            else:
                if reading in hiragana_sentence:

                    for exp in sentence_remove:
                        english = english.replace(exp, "")

                    sentence_list.append(kanji_sentence)
                    english_list.append(english)




    return sentence_list, english_list, form_list

# request_string = "https://jisho.org/api/v1/search/words?keyword={0}".format("????????????")
# res = requests.get(request_string)
# print(res)
#
# get_jisho_data(word,forms,'./data/api_data/????????????.json')
