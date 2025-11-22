import nltk
from nltk.tokenize import sent_tokenize
from pathlib import Path
import re

# === Если ещё не скачан пакет punkt для токенизации ===
nltk.download('punkt')

# Пути
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR.parent / "text_1.txt"
OUTPUT_PATH = BASE_DIR.parent / "files/sentences_1.txt"

# Чтение текста
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Разделяем текст на страницы по шаблону === СТРАНИЦА N (очищено) ===
page_pattern = re.compile(r"=== СТРАНИЦА (\d+) \(очищено\) ===")
pages = page_pattern.split(raw_text)

# pages будет списком вида: ['', '1', 'текст страницы 1...', '2', 'текст страницы 2...', ...]
# поэтому преобразуем в [(номер, текст)]
pages_list = []
for i in range(1, len(pages), 2):
    page_num = int(pages[i])
    page_text = pages[i+1]
    pages_list.append((page_num, page_text))

# Запись результата
with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
    for page_num, page_text in pages_list:
        # очищаем разрывы строк внутри абзацев
        page_text = ' '.join(line.strip() for line in page_text.splitlines() if line.strip())
        # токенизация на предложения
        sentences = sent_tokenize(page_text, language="russian")
        for idx, sent in enumerate(sentences, 1):
            f_out.write(f"{page_num}_{idx}: {sent}\n")

print(f"Готово! Результат сохранен → {OUTPUT_PATH}")
