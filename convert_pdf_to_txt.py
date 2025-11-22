import time
import fitz  # PyMuPDF
from paddleocr import PaddleOCR
import paddle
import numpy as np
import requests
import json

# 🔧 НАСТРОЙКИ
INPUT_PDF_PATH = r"C:\MISIS\graph\text_1_clean.pdf"
OUTPUT_TXT_PATH = r"C:\MISIS\graph\text_1.txt"
DPI = 200

OLLAMA_URL = "http://localhost:11434/api/generate"
LLAMA_MODEL = "llama3.1:8b"


# ----------------------------------------------
#  Функция очистки текста через Llama3.1:8b
# ----------------------------------------------
def clean_text_llama(text: str) -> str:
    prompt = f"""
Вот текст, распознанный из PDF:

{text}

Требуется очистить его:
- исправить ошибки OCR
- убрать мусор, куски таблиц, разметку, линии, нумерацию, повторения
- убрать разрывы строк в середине предложений
- сохранить только чистый связный текст
- ничего не добавлять от себя
- язык оставить русский

Верни только конечный очищенный текст.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLAMA_MODEL,
            "prompt": prompt
        },
        stream=True,
    )

    cleaned = ""
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():
            try:
                obj = json.loads(line)
                cleaned += obj.get("response", "")
            except:
                continue

    return cleaned.strip()


# ----------------------------------------------
#      ОСНОВНАЯ ОБРАБОТКА PDF
# ----------------------------------------------
def pdf_all_pages_paddleocr_to_txt():
    print("📄 Открываю PDF через PyMuPDF...")
    doc = fitz.open(INPUT_PDF_PATH)

    num_pages = doc.page_count
    print(f"✅ В документе {num_pages} страниц, обрабатываю все")

    print("🧠 Paddle устройство:", paddle.device.get_device())

    print("🧠 Инициализирую PaddleOCR на GPU...")
    ocr = PaddleOCR(
        lang="ru",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        device="gpu",
    )

    all_pages_clean = []
    t0 = time.perf_counter()

    for page_index in range(num_pages):
        print(f"🔄 Рендерю страницу {page_index + 1}/{num_pages}...")
        page = doc.load_page(page_index)

        zoom = DPI / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img = np.frombuffer(pix.samples, dtype=np.uint8)
        img = img.reshape(pix.height, pix.width, pix.n)

        print(f"🧠 Распознаю текст на странице {page_index + 1}...")
        results = ocr.predict(img)

        page_lines = []
        for res in results:
            data = res.json
            rec_texts = data.get("res", {}).get("rec_texts", [])
            page_lines.extend(rec_texts)

        raw_text = "\n".join(page_lines)
        print(f"✨ Отправляю страницу {page_index + 1} на очистку в Llama3.1...")

        cleaned_text = clean_text_llama(raw_text)

        all_pages_clean.append(
            f"=== СТРАНИЦА {page_index + 1} (очищено) ===\n{cleaned_text}\n"
        )

    doc.close()

    # Сохраняем всё
    with open(OUTPUT_TXT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(all_pages_clean))

    t1 = time.perf_counter()
    print("\n✅ Готово! Итоговый текст сохранён в:", OUTPUT_TXT_PATH)
    print(f"⏱ Обработка заняла {t1 - t0:.1f} секунд")


if __name__ == "__main__":
    pdf_all_pages_paddleocr_to_txt()
