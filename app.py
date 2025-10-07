from flask import Flask, render_template, request, redirect, url_for
import json, random, os

app = Flask(__name__)

# Пути к файлам
DATA_DIR = "data"
THEORY_FILE = os.path.join(DATA_DIR, "theory.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")


# --- Загрузка данных ---
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# --- Главная страница ---
@app.route("/")
def index():
    theory = load_json(THEORY_FILE)
    topics = list(theory.keys())
    return render_template("index.html", topics=topics)


# --- Теория ---
@app.route("/theory/<topic>")
def theory(topic):
    theory_data = load_json(THEORY_FILE)
    content = theory_data.get(topic, "Теория по данной теме пока отсутствует.")
    return render_template("theory.html", topic=topic, content=content)


# --- Тестирование ---
@app.route("/test/<topic>")
def test(topic):
    questions_data = load_json(QUESTIONS_FILE)
    topic_questions = questions_data.get(topic, [])

    if not topic_questions:
        return f"<h3>По теме «{topic}» пока нет вопросов.</h3>"

    # Перемешиваем вопросы
    random.shuffle(topic_questions)
    return render_template("test.html", topic=topic, questions=topic_questions[:10])


# --- Проверка ответов ---
@app.route("/check", methods=["POST"])
def check():
    topic = request.form.get("topic", "Неизвестная тема")
    questions_data = load_json(QUESTIONS_FILE)
    topic_questions = questions_data.get(topic, [])

    correct = 0
    total = len(topic_questions)

    for i, q in enumerate(topic_questions[:10]):
        answer = request.form.get(f"q{i}")
        if answer == q["answer"]:
            correct += 1

    percent = round(correct / total * 100, 1) if total > 0 else 0
    grade = (
        "Отлично" if percent >= 85 else
        "Хорошо" if percent >= 70 else
        "Удовлетворительно" if percent >= 50 else
        "Неудовлетворительно"
    )

    return render_template(
        "result.html",
        topic=topic,
        correct=correct,
        total=total,
        percent=percent,
        grade=grade
    )


# --- Запуск ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
