import json
import chardet
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR.parent / "files/data_20000.json"
OUTPUT_PATH = BASE_DIR.parent / "files/data_output_20000.json"

def read_json_with_unknown_encoding(path):
    """
    Считывает файл неизвестной кодировки и возвращает нормализованный строковый текст.
    """
    # with open(path, "rb") as f:
    #     raw = f.read()

    # # Определяем кодировку автоматически
    # encoding_guess = chardet.detect(raw)["encoding"]
    # print(f"[INFO] Обнаружена кодировка: {encoding_guess}")

    # try_encodings = [encoding_guess, "utf-8", "cp1251"]

    # for enc in try_encodings:
    #     if enc is None:
    #         continue
    #     try:
    #         print(f"[INFO] Пробуем декодировать как {enc}")
    #         return raw.decode(enc)
    #     except UnicodeDecodeError:
    #         pass

    # # Если всё плохо — декодируем с заменой битых символов
    # print("[WARN] Не удалось точно определить кодировку. Использую 'utf-8' c заменой.")
    # return raw.decode("utf-8", errors="replace")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def save_json_text_as_txt(json_text: str, output_path: str):
    """
    Принимает строку JSON (как текст) и сохраняет её в TXT без потери структуры.
    """
    # Сохраняем текст как есть
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_text)

    print(f"[OK] Текст сохранён в: {output_path}")

def save_json_no_ascii(data: str, output_path: str):

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,   # <-- ВАЖНО! сохраняет кириллицу нормально
            indent=2              # чтобы сохранить красивую структуру
        )

def main():

    json_raw_text = read_json_with_unknown_encoding(INPUT_PATH)
    # save_json_text_as_txt(json_raw_text, OUTPUT_PATH)
    save_json_no_ascii(json_raw_text, OUTPUT_PATH)


if __name__ == "__main__":
    main()
