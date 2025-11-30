import json
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR.parent / "files/merged_2.json"
OUTPUT_PATH = BASE_DIR.parent / "files/memgraph-text-2.json"

# Если у вас файл — раскомментируйте:
with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ==================================================================
# Преобразуем в нужный формат
# ==================================================================

nodes = []
relationships = []

# Сначала создаём все узлы
for id, entity in data["entities"].items():
    node = {
        "id": 130+int(id[1:]),           # убираемый префикс A → 61, 62 и т.д.
        "labels": ["Term"],                     # можно поменять на нужную метку
        "properties": {
            "name": entity,
            "original_id": id
        },
        "type": "node"
    }
    nodes.append(node)

# Теперь создаём отношения
rel_id_counter = 200000  # произвольный старт, чтобы не пересекаться с id узлов

for triple in data["triples"]:
    subj_id = 130+int(triple["subject"][1:])
    obj_ids = triple["object"] if isinstance(triple["object"], list) else [triple["object"]]
    
    # Некоторые предикаты у вас на русском и с подчёркиваниями — нормализуем
    predicate = triple["predicate"].strip().upper()
    predicate = predicate.replace(" ", "_").replace("-", "_")
    # Если хотите более красивые имена — можно добавить словарь переводов
    rel_label = predicate
    
    print(obj_ids)

    for obj in obj_ids:
        obj_id = 130+int(obj[1:])
        
        rel = {
            "id": rel_id_counter,
            "label": rel_label,
            "properties": {},
            "start": subj_id,
            "end": obj_id,
            "type": "relationship"
        }
        relationships.append(rel)
        rel_id_counter += 1

# Собираем всё вместе
result = nodes + relationships

# Сохраняем в файл
with open(OUTPUT_PATH, 'w', encoding='ascii', newline='\n') as f:
    json.dump(
        result,
        f,
        ensure_ascii=True,        # ← ВСЁ в \u041f\u0440\u0438\u0432\u0435\u0442 виде
        indent=2,
        separators=(',', ': '),
        sort_keys=False
    )

print(f"Готово! Создано {len(nodes)} узлов и {len(relationships)} отношений.")
print("Файл:" + str(OUTPUT_PATH))