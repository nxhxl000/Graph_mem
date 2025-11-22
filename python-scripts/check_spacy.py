import spacy
nlp = spacy.load("ru_core_news_lg")
doc = nlp("Привет, как работает токенизация?")
for t in doc:
    print(t.text, t.pos_, t.lemma_)