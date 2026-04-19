# Мини-анкета

Простое full-stack приложение: Flask API и статический frontend без фреймворков. Вопросы задаются на сервере, ответы сохраняются **в памяти процесса** (после перезапуска backend история обнуляется).

## Технологии

- Python 3
- Flask 3
- HTML, CSS, JavaScript (без сборки и без npm)

## Структура проекта

```
dz/
├── backend/
│   ├── app.py              # Flask: GET /questions, POST /answers
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── prompts/                # тексты промптов для сдачи / истории
├── screenshots/            # скриншоты + README с инструкцией
├── README.md
└── .gitignore
```

## Запуск backend

Из корня репозитория (или из папки `backend/`):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Сервер слушает **http://127.0.0.1:5000** (режим `debug=True` для учебного запуска).

## Запуск frontend

Из-за политики браузера к **запросам с `file://`** к другому origin надёжнее открыть страницу через **простой HTTP-сервер** в папке `frontend/`:

```bash
cd frontend
python3 -m http.server 8080
```

В браузере откройте: **http://127.0.0.1:8080**

В `script.js` задан `API_BASE = "http://127.0.0.1:5000"` — он должен совпадать с адресом Flask. Backend отдаёт заголовки **CORS** (`Access-Control-Allow-Origin: *`), чтобы запросы с порта 8080 проходили без ошибки.

## API

### `GET /questions`

**Ответ 200** (пример):

```json
{
  "questions": [
    { "id": "q1", "text": "Как вас зовут?" },
    { "id": "q2", "text": "..." }
  ]
}
```

### `POST /answers`

**Заголовок:** `Content-Type: application/json`

**Тело:**

```json
{
  "answers": [
    { "question_id": "q1", "text": "Иван" },
    { "question_id": "q2", "text": "Учусь в университете" }
  ]
}
```

Требуется **ровно по одному непустому ответу** на каждый известный `question_id` из списка вопросов.

**Успех 201:** `{ "ok": true, "message": "Ответы сохранены", "submissions_count": N }`

**Ошибки 400:** `{ "error": "текст причины" }` — неверный JSON, неизвестный id, пустой текст, не все вопросы и т.д.

## Промпты

Список файлов в `prompts/`:

- `01-initial-generation.md` — постановка задачи и требования к проекту
- `02-bugfix.md` — заготовка под промпты исправлений
- `03-improvements.md` — заготовка под доработки

## Скриншоты

Сделайте два скриншота и положите в `screenshots/` (подробности в `screenshots/README.md`):

| Файл | Содержание |
|------|------------|
| `main-form.png` | Форма с вопросами до отправки |
| `thank-you.png` | Сообщение «Спасибо!» после успешной отправки |

*(После добавления файлов можно вставить в этот раздел картинки Markdown, например `![Форма](screenshots/main-form.png)`.)*

## Что реализовано

- Backend: Flask, жёстко заданные 4 вопроса, in-memory список отправок, валидация JSON и полей, корректные коды ответа, CORS.
- Frontend: загрузка вопросов при открытии, динамические поля, POST JSON, блок успеха/ошибки, после успеха форма скрывается и показывается «Спасибо!».
