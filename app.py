import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Абсолютный путь к questions.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
questions_file = os.path.join(BASE_DIR, "questions.json")

with open(questions_file, "r", encoding="utf-8") as f:
    questions_data = json.load(f)

@app.route("/")
def index():
    topics = list(questions_data.keys())
    return render_template("index.html", topics=topics)

@app.route("/test/<topic>", methods=["GET", "POST"])
def test(topic):
    topic_questions = []

    for level in questions_data.get(topic, {}):
        for q in questions_data[topic][level]:
            topic_questions.append(q)

    random.shuffle(topic_questions)

    if request.method == "POST":
        score = 0
        for i, q in enumerate(topic_questions):
            ans = request.form.get(f"q{i}")
            if ans and int(ans) == q[2]:
                score += 1
        return render_template("result.html", score=score, total=len(topic_questions))

    return render_template("test.html", topic=topic, questions=topic_questions)

@app.route("/theory/<topic>")
def theory(topic):
    # Пока просто заглушка, можно добавить теоретический материал
    return render_template("theory.html", topic=topic)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
