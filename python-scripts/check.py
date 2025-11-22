from pathlib import Path
import re
import nltk

# Загрузка стоп-слов
nltk.download('stopwords')
from nltk.corpus import stopwords

# Пути к файлам
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR.parent / "files/sentences_1_renum.txt"
OUTPUT_PATH = BASE_DIR.parent / "files/sentences_1_no_stopwords.txt"

# Стандартные русские стоп-слова
russian_stopwords = set(stopwords.words('russian'))

# Важные местоимения, которые НЕ удаляем
important_pronouns = {
    # Личные
    'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они',
    'меня', 'тебя', 'его', 'ее', 'нас', 'вас', 'их',
    'мне', 'тебе', 'ему', 'ей', 'нам', 'вам', 'им',
    'мой', 'твой', 'его', 'ее', 'наш', 'ваш', 'их',
    'моё', 'твоё', 'наше', 'ваше',
    'моя', 'твоя', 'наша', 'ваша',
    'мои', 'твои', 'наши', 'ваши',

    # Указательные
    'этот', 'эта', 'это', 'эти', 'тот', 'та', 'то', 'те',
    'такой', 'такая', 'такое', 'такие', 'таков', 'такова', 'таково', 'таковы',

    # Относительные и вопросительные
    'кто', 'что', 'какой', 'какая', 'какое', 'какие',
    'который', 'которая', 'которое', 'которые',
    'чей', 'чья', 'чьё', 'чьи'
}

# Убираем эти местоимения из стандартного списка стоп-слов
russian_stopwords -= important_pronouns

# Функция для удаления стоп-слов
def remove_stopwords(text):
    tokens = re.findall(r'\b\w+\b|[^\w\s]', text, re.UNICODE)
    filtered_tokens = [t for t in tokens if t.lower() not in russian_stopwords]
    return ' '.join(filtered_tokens)

# Чтение входного файла
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    line = line.strip()
    if not line:
        continue

    m = re.match(r"(\d+)_(\d+):\s*(.+)", line)
    if not m:
        new_lines.append(line)
        continue

    page_num, sent_num, sentence_text = m.groups()
    clean_sentence = remove_stopwords(sentence_text)

    new_lines.append(f"{page_num}_{sent_num}: {clean_sentence}")

# Запись результата
with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(new_lines))

print(f"Файл без стоп-слов сохранён: {OUTPUT_PATH}")
