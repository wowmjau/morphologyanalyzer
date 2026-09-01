import spacy
from jamdict import Jamdict

nlp = spacy.load("ja_core_news_sm")

jam = Jamdict()

doc = nlp("私は猫です。ニャー！ 「お前、どこの子だ？」足に纏わりついてきたのは、小さな子猫だった。灰色の縞模様のふわふわした猫だ。 ")

syntax = ""

for token in doc:
    if token.pos_ == "NOUN":
        print("ill try and translate")
        result = jam.lookup(str(token))
        syntax += str(result.entries[0])
    else:
        syntax += str(token.pos_)
    print(token.pos_, end=" ")
    print(token.morph, end=" ")
print("\n" + doc.text)
print(syntax)