from flask import Flask, render_template, request, send_from_directory
import json

app = Flask(__name__)

# Загружаем вопросы и теорию
with open("data/questions.json", encoding="utf-8") as f:
    questions_data = json.load(f)

with open("data/theory.json", encoding="utf-8") as f:
    theory_data = json.load(f)


@app.route("/")
def index():
    topics = list(questions_data.keys())
    return render_template("index.html", topics=topics)


@app.route("/test/<topic>/<difficulty>", methods=["GET", "POST"])
def test(topic, difficulty):
    # Берем список вопросов по теме и уровню сложности
    topic_questions = questions_data.get(topic, {}).get(difficulty, [])
    if request.method == "POST":
        score = 0
        for i, q in enumerate(topic_questions):
            selected = request.form.get(f"q{i}")
            if selected is not None and int(selected) == q[2]:
                score += 1
        return render_template("result.html", topic=topic, difficulty=difficulty,
                               score=score, total=len(topic_questions))
    return render_template("test.html", topic=topic, difficulty=difficulty, questions=topic_questions)


@app.route("/theory/<topic>")
def theory(topic):
    content = theory_data.get(topic)
    if content is None:
        return "Тема не найдена", 404
    return render_template("theory.html", topic=topic, content=content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
