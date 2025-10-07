from flask import Flask, render_template
import json, random

app = Flask(__name__)

# Загружаем JSON
with open("questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@app.route("/")
def index():
    topics = list(data.keys())
    return render_template("index.html", topics=topics)

@app.route("/theory")
def theory():
    return render_template("theory.html")

@app.route("/test/<topic>")
def test(topic):
    if topic not in data:
        return "Тема не найдена", 404

    # Получаем все уровни сложности
    levels = data[topic]
    questions = []

    # Собираем все вопросы из всех уровней
    for lvl in levels:
        for q in levels[lvl]:
            questions.append({
                "question": q[0],
                "options": q[1],
                "answer": q[2]
            })

    random.shuffle(questions)  # Перемешиваем вопросы
    return render_template("test.html", topic=topic, questions=questions)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
