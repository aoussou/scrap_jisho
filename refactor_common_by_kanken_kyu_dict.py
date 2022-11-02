import os
import json

data = json.load(open("./data/common_2級.json"))

new_dict = dict()
count_ = 0
for k, v in data.items():
    dict_ = dict()

    dict_["question"] = k
    dict_["target"] = k
    dict_["answer"] = ''.join(v["hiragana"])
    dict_["level"] = v["kanken_kyu"]
    new_dict[count_] = dict_

    count_ += 1

with open(os.path.join('./data', 'common_yomi.json'), 'w') as fp:
    json.dump(new_dict, fp)
fp.close()
