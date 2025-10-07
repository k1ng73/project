from flask import Flask, render_template, request
import json
import random
import os

app = Flask(__name__)

# Пути к файлам
QUESTIONS_FILE = os.path.join("data", "questions.json")
THEORY_FILE = os.path.join("data", "theory.json")

# Загружаем вопросы и теорию
with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    questions_data = json.load(f)

with open(THEORY_FILE, "r", encoding="utf-8") as f:
    theory_data = json.load(f)

@app.route("/")
def index():
    topics = list(questions_data.keys())
    return render_template("index.html", topics=topics)

@app.route("/test/<topic>", methods=["GET", "POST"])
def test(topic):
    if topic not in questions_data:
        return "Тема не найдена", 404

    level = "Лёгкий"  # Можно позже добавить выбор уровня
    topic_questions = questions_data[topic][level]
    random.shuffle(topic_questions)

    if request.method == "POST":
        score = 0
        for i, q in enumerate(topic_questions):
            selected = request.form.get(f"q{i}")
            if selected is not None and int(selected) == q[2]:
                score += 1
        return render_template("result.html", score=score, total=len(topic_questions))

    return render_template("test.html", topic=topic, questions=topic_questions)

@app.route("/theory/<topic>")
def theory(topic):
    if topic not in theory_data:
        return "Тема не найдена", 404
    content = theory_data[topic]
    return render_template("theory.html", topic=topic, content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
