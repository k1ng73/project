from flask import Flask, render_template, request
import json, random, os

app = Flask(__name__)

# Загружаем данные
def load_data():
    with open("data/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    with open("data/theory.json", "r", encoding="utf-8") as f:
        theory = json.load(f)
    return questions, theory

questions, theory = load_data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/theory")
def show_theory():
    return render_template("theory.html", theory=theory)

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        correct = 0
        total = len(questions)
        for i, q in enumerate(questions):
            user_answer = request.form.get(f"q{i}")
            if user_answer == q["correct"]:
                correct += 1
        percent = round(correct / total * 100, 1)
        return render_template("result.html", correct=correct, total=total, percent=percent)
    else:
        random.shuffle(questions)
        selected = questions[:10]
        return render_template("test.html", questions=selected)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
