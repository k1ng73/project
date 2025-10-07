from flask import Flask, render_template, request, redirect, url_for
import json
import random
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
QUESTIONS_FILE = BASE_DIR / "questions.json"
RESULTS_FILE = BASE_DIR / "results.json"

# ------------------- Утилиты -------------------
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def grade_from_pct(pct: float) -> int:
    if pct < 50:
        return 2
    elif pct < 70:
        return 3
    elif pct < 85:
        return 4
    return 5

# ------------------- Загрузка вопросов -------------------
questions = load_json(QUESTIONS_FILE)

# ------------------- Главная страница -------------------
@app.route("/")
def index():
    topics = list(questions.keys())
    return render_template("index.html", topics=topics)

# ------------------- Тест по теме -------------------
@app.route("/test/<topic>", methods=["GET", "POST"])
def test(topic):
    all_questions = questions.get(topic, {})

    # Превращаем словарь в список
    topic_questions = []
    for level_data in all_questions.values():
        if isinstance(level_data, dict):
            topic_questions.extend(list(level_data.values()))
        elif isinstance(level_data, list):
            topic_questions.extend(level_data)

    # Перемешиваем
    random.shuffle(topic_questions)

    if request.method == "POST":
        # Получаем ответы из формы
        answers = request.form
        correct = 0
        for idx, q in enumerate(topic_questions):
            # Если в JSON q = [текст, варианты, правильный индекс]
            if str(idx) in answers and answers[str(idx)] != "":
                if int(answers[str(idx)]) == q[2]:
                    correct += 1
        total = len(topic_questions)
        pct = (correct / total) * 100
        grade = grade_from_pct(pct)

        # Сохраняем результат
        result = {
            "topic": topic,
            "correct": correct,
            "total": total,
            "percent": round(pct, 2),
            "grade": grade
        }
        results = load_json(RESULTS_FILE)
        if not isinstance(results, list):
            results = []
        results.append(result)
        save_json(RESULTS_FILE, results)

        return render_template("result.html", result=result)

    return render_template("test.html", topic=topic, questions=topic_questions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
