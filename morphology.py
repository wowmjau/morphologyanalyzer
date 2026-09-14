import spacy
from stressrnn import StressRNN

nlp = spacy.load("ru_core_news_sm")
stress_rnn = StressRNN()

doc = nlp("Пачка сигарет! кот коту аргументирование")


syntax = ""

script = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "ë",
    "ж": "ž",
    "з": "z",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "c",
    "ч": "č",
    "ш": "š",
    "щ": "šč",
    "ъ": "ʺ",
    "ы": "y",
    "ь": "ʹ",
    "э": "ė",
    "ю": "ju",
    "я": "ja",
}

glossterms = {
    # nouns
    "Inan": "INAN",
    "Anim": "AN",
    "Nom": "NOM",
    "Acc": "ACC",
    "Gen": "GEN",
    "Dat": "DAT",
    "Ins": "INS",
    "Masc": "M",
    "Fem": "F",
    "Neut": "N",
    "Sing": "SG",
    "Plur": "PL",
}

'''
def dictionarycheck(word):
    result = jmd.lookup(str(word))
    for entry in result.entries:
        sense = entry.senses[0]
        text = str(sense.glosses[0])
        p1 = text.find("'")
        p2 = text.find("'", p1 + 1)
        return text[p1 + 1:p2]
'''

def stress(text):
    stressed_text = stress_rnn.put_stress(text, stress_symbol='+', accuracy_threshold=0.75, replace_similar_symbols=True)
    stressed_text = list(stressed_text)
    for index in range(len(stressed_text)):
        if stressed_text[index] == "+":
            stressed_text[index] = "́"
    return "".join(stressed_text)

def romanize(text):
    return "".join(script.get(char, " ") for char in str(text).lower())

def glossfinder(text): # put token.morph in here
    case = ""
    for item in str(text).split("|"):
        case += f".{glossterms.get(item.split("=")[1])}"
    return case


for token in doc:
    if token.pos_ == "NOUN":
        print("ill try and translate")
        result = "meow"
        syntax += str(result + glossfinder(token.morph) + " ")
    elif token.pos_ == "PRON":
        if str(token) == "私":
            syntax += "I "
    elif token.pos_ == "ADP":
        syntax += script.get(str(token), "idk ")
    elif token.pos_ == "PUNCT":
        syntax += "| "
    else:
        syntax += str(token.pos_ + " ")
    print(token.pos_, end=" ")


print(f"\nOriginal text: {doc.text}")
print(f"With stress:   {stress(str(doc))}")
print(f"Romanization:  {romanize(str(doc))}")
print(f"Gloss:         {syntax}")
