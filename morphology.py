import spacy
from jmdictpy import JMDict

nlp = spacy.load("ja_core_news_sm")

jmd = JMDict()

doc = nlp("私は猫です。ニャー！ 「お前、どこの子だ？」足に纏わりついてきたのは、小さな子猫だった。灰色の縞模様のふわふわした猫だ。 ")

syntax = ""

particles = {
    "は" : "SUBJ ",
}

def dictionarycheck(word):
    result = jmd.lookup(str(word))
    for entry in result.entries:
        sense = entry.senses[0]
        text = str(sense.glosses[0])
        p1 = text.find("'")
        p2 = text.find("'", p1 + 1)
        return text[p1 + 1:p2]

for token in doc:
    if token.pos_ == "NOUN":
        print("ill try and translate")
        result =  dictionarycheck(token)
        syntax += str(result + " ")
    elif token.pos_ == "PRON":
        if str(token) == "私":
            syntax += "I "
    elif token.pos_ == "ADP":
        syntax += particles.get(str(token), "idk ")
    else:
        syntax += str(token.pos_ + " ")
    print(token.pos_, end=" ")
    print(token.morph, end=" ")
print("\n" + doc.text)
print(syntax)