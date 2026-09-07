"""Questionnaire routes.

One question per screen, server-rendered (matches the "Question X of 18"
mockup). Answers accumulate in the Flask session as the user moves through
the wizard -- no database yet (that's a later milestone; see CLAUDE.md).

Items are the WHO Adult ADHD Self-Report Scale (ASRS-v1.1) Symptom
Checklist, Parts A and B (18 items total), referenced as the project's
foundational screening instrument in
docs/ADHD_Project_Master_Specification.md §12. Wording/response mapping is
preserved as published; this is a self-report screening component, not a
diagnosis (§12, CLAUDE.md non-negotiable rules).
"""

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

questionnaire_bp = Blueprint("questionnaire", __name__)

OPTIONS = ["Never", "Rarely", "Sometimes", "Often", "Very Often"]

# ASRS-v1.1 Symptom Checklist -- Part A (1-6), Part B (7-18).
QUESTIONS = [
    "How often do you have trouble wrapping up the final details of a "
    "project, once the challenging parts have been done?",
    "How often do you have difficulty getting things in order when you "
    "have to do a task that requires organization?",
    "How often do you have problems remembering appointments or "
    "obligations?",
    "When you have a task that requires a lot of thought, how often do "
    "you avoid or delay getting started?",
    "How often do you fidget or squirm with your hands or feet when you "
    "have to sit down for a long time?",
    "How often do you feel overly active and compelled to do things, "
    "like you were driven by a motor?",
    "How often do you make careless mistakes when you have to work on a "
    "boring or difficult project?",
    "How often do you have difficulty keeping your attention when you "
    "are doing boring or repetitive work?",
    "How often do you have difficulty concentrating on what people say "
    "to you, even when they are speaking to you directly?",
    "How often do you misplace or have difficulty finding things at "
    "home or at work?",
    "How often are you distracted by activity or noise around you?",
    "How often do you leave your seat in meetings or other situations "
    "in which you are expected to remain seated?",
    "How often do you feel restless or fidgety?",
    "How often do you have difficulty unwinding and relaxing when you "
    "have time to yourself?",
    "How often do you find yourself talking too much when you are in "
    "social situations?",
    "When you're in a conversation, how often do you find yourself "
    "finishing the sentences of the people you are talking to, before "
    "they can finish them themselves?",
    "How often do you have difficulty waiting your turn in situations "
    "when turn taking is required?",
    "How often do you interrupt others when they are busy?",
]

TOTAL = len(QUESTIONS)
SESSION_KEY = "questionnaire_answers"


@questionnaire_bp.route("/questionnaire")
def index():
    session.setdefault(SESSION_KEY, {})
    return redirect(url_for("questionnaire.question", n=1))


@questionnaire_bp.route("/questionnaire/<int:n>", methods=["GET", "POST"])
def question(n):
    if n < 1 or n > TOTAL:
        abort(404)

    answers = session.setdefault(SESSION_KEY, {})
    error = None

    if request.method == "POST":
        action = request.form.get("action")
        answer = request.form.get("answer")

        if action == "previous":
            if answer in OPTIONS:
                answers[str(n)] = answer
                session.modified = True
            if n == 1:
                return redirect(url_for("main.consent"))
            return redirect(url_for("questionnaire.question", n=n - 1))

        if action == "next":
            if answer not in OPTIONS:
                error = "Please select an answer to continue."
            else:
                answers[str(n)] = answer
                session.modified = True
                if n == TOTAL:
                    return redirect(url_for("questionnaire.complete"))
                return redirect(url_for("questionnaire.question", n=n + 1))

    return render_template(
        "questionnaire.html",
        question_text=QUESTIONS[n - 1],
        options=OPTIONS,
        n=n,
        total=TOTAL,
        percent=round(n / TOTAL * 100),
        selected=answers.get(str(n)),
        error=error,
    )


@questionnaire_bp.route("/questionnaire/complete")
def complete():
    answers = session.get(SESSION_KEY, {})
    return render_template(
        "questionnaire_complete.html",
        answered=len(answers),
        total=TOTAL,
    )
