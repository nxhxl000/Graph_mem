from pathlib import Path
import re
import nltk

# Загружаем стоп-слова
nltk.download('stopwords')
from nltk.corpus import stopwords

# Пути к файлам
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR.parent / "files/sentences_1_renum.txt"
OUTPUT_PATH = BASE_DIR.parent / "files/sentences_1_no_stopwords.txt"

russian_stopwords = set(stopwords.words('russian'))

# Функция для удаления стоп-слов
def remove_stopwords(text):
    # Разбиваем на слова и знаки препинания
    tokens = re.findall(r'\b\w+\b|[^\w\s]', text, re.UNICODE)
    filtered_tokens = [t for t in tokens if t.lower() not in russian_stopwords]
    result = ' '.join(filtered_tokens)
    # Убираем лишние пробелы перед знаками препинания
    # result = re.sub(r'\s+([,.:;!?])', r'\1', result)
    # Убираем лишние двойные пробелы
    result = re.sub(r'\s{2,}', ' ', result)
    return result

# Чтение файла
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Разбор индекса и текста
    m = re.match(r"(\d+)_(\d+):\s*(.+)", line)
    if not m:
        new_lines.append(line)
        continue

    page_num, sent_num, sentence_text = m.groups()
    clean_sentence = remove_stopwords(sentence_text)
    new_lines.append(f"{page_num}_{sent_num}: {clean_sentence}")

# Запись в файл
with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(new_lines))

print(f"Файл без стоп-слов сохранён: {OUTPUT_PATH}")
