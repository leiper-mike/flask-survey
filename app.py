from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey
app = Flask(__name__)
app.secret_key = 'abc123'
@app.route('/')
def base():
    return render_template("root.html", surveyTitle = satisfaction_survey.title, surveyInstructions = satisfaction_survey.instructions)

@app.route('/questions/<int:num>')
def question(num):
    responses = session["answers"]
    if(num == len(satisfaction_survey.questions)):
        if(session["finished"]):
            flash("You have already completed the survey")
            return redirect("/thanks")
        session["finished"] = True
        return redirect("/thanks")
    if(not (num == len(responses)) or num >= len(satisfaction_survey.questions)):
        flash("Invalid question ID")
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[num]
    return render_template("question.html", questionText = question.question, questionChoices = question.choices, allow_text = question.allow_text, surveyTitle = satisfaction_survey.title)

@app.route('/answer', methods=["POST"])
def answer():
    answers = session["answers"]
    answers.append(request.form["answer"])
    session["answers"] = answers
    return redirect(f"/questions/{len(answers)}")

@app.route('/thanks')
def thanks():
    responses = session["answers"]
    if(not len(responses) == len(satisfaction_survey.questions)):
        flash("You must complete the survey before we thank you.")
        return redirect(f"questions/{len(responses)}")
    return render_template("thanks.html", surveyName = satisfaction_survey.title)

@app.route("/start", methods=["POST"])
def start():
    session["answers"] = []
    session["finished"] = False
    return redirect("/questions/0")