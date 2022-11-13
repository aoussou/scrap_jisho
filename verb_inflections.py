verb = "飛ぶ"
type = "godan"

stem_dict = dict()

u_dict = dict()
u_dict["i"] = "い"
u_dict["a"] = "わ"
u_dict["e"] = "え"
u_dict["te"] = "って"
u_dict["past"] = "った"

ku_dict = dict()
ku_dict["i"] = "く"
ku_dict["a"] = "か"
ku_dict["e"] = "け"
ku_dict["te"] = "いて"
ku_dict["past"] = "いた"

gu_dict = dict()
gu_dict["i"] = "ぐ"
gu_dict["a"] = "が"
gu_dict["e"] = "げ"
gu_dict["te"] = "いで"
gu_dict["past"] = "いだ"

su_dict = dict()
su_dict["i"] = "し"
su_dict["a"] = "さ"
su_dict["e"] = "せ"
su_dict["te"] = "して"
su_dict["past"] = "した"

tu_dict = dict()
tu_dict["i"] = "ち"
tu_dict["a"] = "た"
tu_dict["e"] = "て"
tu_dict["te"] = "って"
tu_dict["past"] = "った"

nu_dict = dict()
nu_dict["i"] = "に"
nu_dict["a"] = "な"
nu_dict["e"] = "ね"
nu_dict["te"] = "んで"
nu_dict["past"] = "んだ"

bu_dict = dict()
bu_dict["i"] = "び"
bu_dict["a"] = "ば"
bu_dict["e"] = "べ"
bu_dict["te"] = "んで"
bu_dict["past"] = "んだ"

mu_dict = dict()
mu_dict["i"] = "み"
mu_dict["a"] = "ま"
mu_dict["e"] = "め"
mu_dict["te"] = "んで"
mu_dict["past"] = "んだ"

ru_dict = dict()
ru_dict["i"] = "り"
ru_dict["a"] = "ら"
ru_dict["e"] = "れ"
ru_dict["te"] = "って"
ru_dict["past"] = "った"

id_dict = dict()
id_dict["i"] = ""
id_dict["a"] = ""
id_dict["e"] = "られ"
id_dict["te"] = "て"
id_dict["past"] = "た"
id_dict["imperative"] = "ろ"

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
endings_dict["id"] = id_dict


def get_endings(verb, is_ichidan):
    if is_ichidan:
        endings = endings_dict["id"]
    else:
        endings = endings_dict[verb[-1]]
        endings["imperative"] = endings["e"]

    return endings


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
