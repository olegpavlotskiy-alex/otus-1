"""
Мини-анкета: простой Flask API для вопросов и ответов (хранение в памяти процесса).
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Вопросы анкеты (жёстко заданные)
QUESTIONS = [
    {"id": "q1", "text": "Как вас зовут?"},
    {"id": "q2", "text": "Чем вы занимаетесь (учёба, работа)?"},
    {"id": "q3", "text": "Какой язык программирования изучаете сейчас?"},
    {"id": "q4", "text": "Что вам нравится в разработке больше всего?"},
]

VALID_QUESTION_IDS = {q["id"] for q in QUESTIONS}

# Ответы пользователей: список записей вида {"answers": [...]}
answers_storage: list[dict] = []


@app.after_request
def add_cors_headers(response):
    """CORS для локального запуска (frontend на другом порту или file://)."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/questions", methods=["GET"])
def get_questions():
    return jsonify({"questions": QUESTIONS}), 200


@app.route("/answers", methods=["OPTIONS"])
def answers_preflight():
    return "", 204


@app.route("/answers", methods=["POST"])
def post_answers():
    if not request.is_json:
        return jsonify({"error": "Ожидается JSON с заголовком Content-Type: application/json"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Некорректный JSON"}), 400

    if "answers" not in data:
        return jsonify({"error": "Поле 'answers' обязательно"}), 400

    answers = data["answers"]
    if not isinstance(answers, list):
        return jsonify({"error": "Поле 'answers' должно быть массивом"}), 400

    if len(answers) == 0:
        return jsonify({"error": "Список ответов не должен быть пустым"}), 400

    normalized = []
    seen_ids = set()

    for i, item in enumerate(answers):
        if not isinstance(item, dict):
            return jsonify({"error": f"Элемент {i} должен быть объектом"}), 400
        if "question_id" not in item or "text" not in item:
            return jsonify(
                {"error": f"Элемент {i}: нужны поля 'question_id' и 'text'"}
            ), 400

        qid = item["question_id"]
        text = item["text"]

        if not isinstance(qid, str) or not qid.strip():
            return jsonify({"error": f"Элемент {i}: 'question_id' должен быть непустой строкой"}), 400
        if qid not in VALID_QUESTION_IDS:
            return jsonify({"error": f"Неизвестный question_id: {qid}"}), 400
        if qid in seen_ids:
            return jsonify({"error": f"Повтор question_id: {qid}"}), 400
        seen_ids.add(qid)

        if not isinstance(text, str):
            return jsonify({"error": f"Элемент {i}: 'text' должен быть строкой"}), 400
        stripped = text.strip()
        if not stripped:
            return jsonify({"error": f"Элемент {i}: ответ не может быть пустым"}), 400

        normalized.append({"question_id": qid, "text": stripped})

    if seen_ids != VALID_QUESTION_IDS:
        missing = VALID_QUESTION_IDS - seen_ids
        return jsonify({"error": f"Не на все вопросы дан ответ. Не хватает: {sorted(missing)}"}), 400

    answers_storage.append({"answers": normalized})
    return jsonify({"ok": True, "message": "Ответы сохранены", "submissions_count": len(answers_storage)}), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
