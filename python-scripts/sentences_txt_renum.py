from pathlib import Path
import re

# Пути
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR.parent / "files/sentences_2.txt"
OUTPUT_PATH = BASE_DIR.parent / "files/sentences_2_renum.txt"

# Чтение
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
current_page = None
sent_idx = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    # Разделяем текущий индекс от текста
    m = re.match(r"(\d+)_(\d+):\s*(.+)", line)
    if not m:
        # если строка не соответствует формату, просто добавляем её
        new_lines.append(line)
        continue

    page_num = int(m.group(1))
    sentence_text = m.group(3)

    if page_num != current_page:
        # новая страница → сбрасываем счетчик предложений
        current_page = page_num
        sent_idx = 1
    else:
        sent_idx += 1

    new_lines.append(f"{page_num}_{sent_idx}: {sentence_text}")

# Запись обновленного файла
with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(new_lines))

print(f"Обновленные индексы сохранены → {OUTPUT_PATH}")
