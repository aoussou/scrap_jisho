verb = "飛ぶ"
type = "godan"

stem_dict = dict()

u_dict = dict()
u_dict["u-form"] = "う"
u_dict["i-form"] = "い"
u_dict["a-form"] = "わ"
u_dict["e-form"] = "え"
u_dict["o-form"] = "お"
u_dict["te"] = "って"
u_dict["past"] = "った"

ku_dict = dict()
ku_dict["u-form"] = "く"
ku_dict["i-form"] = "き"
ku_dict["a-form"] = "か"
ku_dict["e-form"] = "け"
ku_dict["o-form"] = "こ"
ku_dict["te"] = "いて"
ku_dict["past"] = "いた"

gu_dict = dict()
gu_dict["u-form"] = "ぐ"
gu_dict["i-form"] = "ぎ"
gu_dict["a-form"] = "が"
gu_dict["e-form"] = "げ"
gu_dict["o-form"] = "ご"
gu_dict["te"] = "いで"
gu_dict["past"] = "いだ"

su_dict = dict()
su_dict["u-form"] = "す"
su_dict["i-form"] = "し"
su_dict["a-form"] = "さ"
su_dict["e-form"] = "せ"
su_dict["o-form"] = "そ"
su_dict["te"] = "して"
su_dict["past"] = "した"

tu_dict = dict()
tu_dict["u-form"] = "つ"
tu_dict["i-form"] = "ち"
tu_dict["a-form"] = "た"
tu_dict["e-form"] = "て"
tu_dict["o-form"] = "と"
tu_dict["te"] = "って"
tu_dict["past"] = "った"

nu_dict = dict()
nu_dict["u-form"] = "ぬ"
nu_dict["i-form"] = "に"
nu_dict["a-form"] = "な"
nu_dict["e-form"] = "ね"
nu_dict["o-form"] = "の"
nu_dict["te"] = "んで"
nu_dict["past"] = "んだ"

bu_dict = dict()
bu_dict["u-form"] = "ぶ"
bu_dict["i-form"] = "び"
bu_dict["a-form"] = "ば"
bu_dict["e-form"] = "べ"
bu_dict["o-form"] = "ぼ"
bu_dict["te"] = "んで"
bu_dict["past"] = "んだ"

mu_dict = dict()
mu_dict["u-form"] = "む"
mu_dict["i-form"] = "み"
mu_dict["a-form"] = "ま"
mu_dict["e-form"] = "め"
mu_dict["o-form"] = "も"
mu_dict["te"] = "んで"
mu_dict["past"] = "んだ"

ru_dict = dict()
ru_dict["u-form"] = "る"
ru_dict["i-form"] = "り"
ru_dict["a-form"] = "ら"
ru_dict["e-form"] = "れ"
ru_dict["o-form"] = "ろ"
ru_dict["te"] = "って"
ru_dict["past"] = "った"


endings_dict = dict()
endings_dict["う"] = u_dict
endings_dict["く"] = ku_dict
endings_dict["ぐ"] = gu_dict
endings_dict["す"] = su_dict
endings_dict["つ"] = tu_dict
endings_dict["ぬ"] = nu_dict
endings_dict["ぶ"] = bu_dict
endings_dict["む"] = mu_dict
endings_dict["る"] = ru_dict
# endings_dict["id"] = id_dict


def get_endings(verb, is_ichidan):
    forms = dict()
    stem = verb[:-1]

    if is_ichidan:
        forms["dictionary"] = verb
        forms["te"] = stem + "て"
        forms["past"] = stem + "た"
        forms["negative"] = stem + "な"
        forms["negative-old"] = stem + "ぬ"
        forms["negative-continous"] = stem + "ず"
        forms["masu-form"] = stem
        forms["masu"] = stem + "ま"
        forms["volitional"] = stem + "よう"
        forms["imperative"] = stem + "ろ"
        forms["potential"] = stem + "られ"
        forms["passive"] = stem + "られ"
        forms["hypothetical"] = stem + "れば"


    else:
        endings = endings_dict[verb[-1]]

        forms["dictionary"] = verb
        forms["te"] = stem + endings["te"]
        forms["past"] = stem + endings["past"]
        forms["negative"] = stem + endings["a-form"] + "な"
        forms["negative-old"] = stem + endings["a-form"] + "ぬ"
        forms["negative-continous"] = stem + endings["a-form"] + "ず"
        forms["masu-form"] = stem + endings["i-form"]
        forms["masu"] = stem + endings["i-form"] + "ま"
        forms["volitional"] = stem + endings["o-form"] + "う"
        forms["imperative"] = stem + endings["e-form"]
        forms["potential"] = stem + endings["e-form"]
        forms["passive"] = endings["a-form"] + "れ"
        forms["hypothetical"] = endings["e-form"] + "ば"

    return forms


# godan_verb_list = ["失う", "聴く", "泳ぐ", "話す", "立つ", "死ぬ", "選ぶ", "好む", "喋る"]


def get_forms(verb, is_ichidan):

    forms_dict = dict()

    endings = get_endings(verb, is_ichidan)
    for v, k in endings.items():
        forms_dict[v] = verb[:-1] + k
        # all_forms.append(verb[:-1] + k)

    return forms_dict


# for verb in godan_verb_list:
#
#     endings = get_endings(verb, False)
#
#
#     print("*" * 10)
#     print("verb", verb)
#     for v, k in endings.items():
#         print(v, verb[:-1] + k)
