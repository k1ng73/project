from flask import Flask, render_template, request
import json
import random
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Папка проекта
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
QUESTIONS_FILE = DATA_DIR / "questions.json"
RESULTS_FILE = BASE_DIR / "results.json"

# -------------------- Утилиты --------------------
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

# Загружаем вопросы
questions = load_json(QUESTIONS_FILE)

# -------------------- Главная страница --------------------
@app.route("/")
def index():
    topics = list(questions.keys())
    return render_template("index.html", topics=topics)

# -------------------- Тест по теме --------------------
@app.route("/test/<topic>", methods=["GET", "POST"])
def test(topic):
    all_levels = questions.get(topic, {})  # {'Лёгкий': {'0': [...], '1': [...]}, ...}

    # Собираем все вопросы в один список
    topic_questions = []
    for level_questions in all_levels.values():
        if isinstance(level_questions, dict):
            topic_questions.extend(level_questions.values())
        elif isinstance(level_questions, list):
            topic_questions.extend(level_questions)

    topic_questions = list(topic_questions)
    random.shuffle(topic_questions)

    if request.method == "POST":
        answers = request.form
        correct = 0
        for idx, q in enumerate(topic_questions):
            if str(idx) in answers and answers[str(idx)] != "":
                if int(answers[str(idx)]) == q[2]:
                    correct += 1
        total = len(topic_questions)
        pct = (correct / total) * 100
        grade = grade_from_pct(pct)

        # Сохраняем результат
        result = {
            "datetime": datetime.now().isoformat(timespec="seconds"),
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

# -------------------- Страница с теорией --------------------
@app.route("/theory")
def theory():
    theory_data = load_json(DATA_DIR / "theory.json")
    return render_template("theory.html", theory=theory_data)

# -------------------- Запуск --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
