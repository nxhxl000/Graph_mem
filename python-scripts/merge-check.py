import os, json
from collections import Counter
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR.parent / "files-text-1-deepseek"

all_texts = []

for file in os.listdir(INPUT_DIR):
    if file.endswith(".json"):
        with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
            data = json.load(f)
            for ent in data["entities"]:
                all_texts.append(ent["text"].strip().lower())

counter = Counter(all_texts)

print("Всего сущностей:", len(all_texts))
print("Уникальных:", len(set(all_texts)))
print("\nТоп-20 повторяющихся:")
for text, cnt in counter.most_common(20):
    print(cnt, "-", text)
