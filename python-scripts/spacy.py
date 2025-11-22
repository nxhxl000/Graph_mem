from pathlib import Path
import nltk
from pymorphy2 import MorphAnalyzer

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR.parent / "text_2.txt"

nltk.download('punkt')
nltk.download('punkt')

morph = MorphAnalyzer()

with open(FILE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

tokens = nltk.word_tokenize(text, language="russian")

for t in tokens:
    p = morph.parse(t)[0]
    print(
        t,            # токен
        p.normal_form, # лемма
        p.tag.POS     # часть речи
    )
