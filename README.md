# Graph Mem

Graph mem project

---

## 📁 Структура проекта

```bash
Graph_mem/
├─ environment.yml          # Конфиг conda-окружения (Python + инструменты)
```

---

## ⚙️ Виртуальное окружение (conda)

### 1) Создать окружение

```bash
conda env create -f environment.yml
```

### 2) Активировать окружение

```bash
conda activate graph_mem_reco
```

### 3) Обновить окружение (если `environment.yml` изменился)

```bash
conda env update -f environment.yml --prune
```

### 4) Установить одну из моделей для русского языка внутри окружения

#### модель ru_core_news_lg

```bash
python -m spacy download ru_core_news_lg
```

#### модель ru_core_news_md

```bash
python -m spacy download ru_core_news_md
```

---

## Проверка установки SpaCy

```bash
python python-scripts\check_spacy.py
```

---

## установка Memgraph

1) Запустить Docker

2) установите снимок

```bash
iwr https://windows.memgraph.com | iex
```

3) посмотреть CONTAINER ID

```bash
docker ps
```

4) запустить CLI контейнера

```bash
docker exec -it <CONTAINER_ID> bash
```

5) перенос файла (файл в самой папке)

```bash
docker cp data_json_utils.json <CONTAINER_ID>:/var/lib/memgraph/
docker cp data_import_util.json <CONTAINER_ID>:/var/lib/memgraph/
```

<CONTAINER_ID>
docker cp data.json 53c374aef99e:/path/to/

docker cp memgraph-text-1.json 53c374aef99e:/var/lib/memgraph/

---

## ✅ Быстрый старт (после клонирования)

```bash
conda activate graph_mem_reco
```

---

## 💡 Примечания

- 
