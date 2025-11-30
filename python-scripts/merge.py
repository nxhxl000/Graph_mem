import os
import json
from collections import OrderedDict
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR.parent / "files-text-1-deepseek"
OUTPUT_FILE = BASE_DIR.parent / "files/merged.json"

def load_all_files():
    files = []
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".json"):
            with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
                files.append(json.load(f))
    return files

def merge_files(files):
    merged_entities = OrderedDict()     # id → {id, text}
    text_to_id = {}                     # text → canonical id
    merge_map = {}                      # old_id → new_id
    merged_triples = []

    # --------------- 1. Collect entities
    for file in files:
        for ent in file["entities"]:
            text = ent["text"].strip().lower()

            if text in text_to_id:
                # Already exists → mark replacement
                canonical_id = text_to_id[text]
                merge_map[ent["id"]] = canonical_id
            else:
                # New entity
                merged_entities[ent["id"]] = ent
                text_to_id[text] = ent["id"]

    # --------------- 2. Expand merge_map with identity mapping
    #    so that unknown ids remain unchanged
    for eid in merged_entities.keys():
        merge_map.setdefault(eid, eid)

    # --------------- 3. Collect triples with ID replacement
    for file in files:
        for tr in file["triples"]:
            new_subject = merge_map.get(tr["subject"], tr["subject"])
            new_predicate = tr["predicate"]

            # object may be string or list
            if isinstance(tr["object"], list):
                new_object = [merge_map.get(o, o) for o in tr["object"]]
            else:
                new_object = merge_map.get(tr["object"], tr["object"])

            merged_triples.append({
                "subject": new_subject,
                "predicate": new_predicate,
                "object": new_object
            })

    # --------------- 4. Remove duplicate entities after merging
    final_entities = list({v["text"].lower(): v for v in merged_entities.values()}.values())

    return {
        "entities": final_entities,
        "triples": merged_triples
    }


if __name__ == "__main__":
    print("Загружаю файлы...")
    files = load_all_files()

    print(f"Файлов найдено: {len(files)}")

    result = merge_files(files)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Готово! Результат записан в {OUTPUT_FILE}")
