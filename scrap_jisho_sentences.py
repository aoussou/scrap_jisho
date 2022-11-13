import os
import re
import pandas as pd
save_dir_jisho_pages = "./data/sentences/掻く #sentences - Jisho.org"
path = os.path.join(save_dir_jisho_pages)

kanji_sentence_remove = [
    """      """,
    """\n""",
    """<li class="clearfix">""",
    """<span class="unlinked">""",
    """</span>""",
    """</li>""",
    """<span class="unlinked">"""
]

furigana = pd.read_csv("./data/hiragana.csv", header=None)
hiragana_char_list = list(furigana.iloc[:, 0])

with open(path) as f:
    lines = f.readlines()

furigana_span = """<span\s+class\="furigana">(?:(?!</span>)(?:.|\n))*</span>"""



sentence_identifier = """<ul class="japanese_sentence japanese japanese_gothic clearfix" lang="ja">"""
for i, l in enumerate(lines):

    if sentence_identifier in l:

        sentence_line = lines[i + 1]
        print(sentence_line)
        kanji_sentence = re.sub(furigana_span, '', sentence_line)
        print(kanji_sentence)


        for exp in kanji_sentence_remove:
            kanji_sentence = kanji_sentence.replace(exp, "")
        print(kanji_sentence)

        hiragana_sentence= ""

        for c in sentence_line:
            if c in hiragana_char_list:
                hiragana_sentence += c
        print(hiragana_sentence)
        STOP
