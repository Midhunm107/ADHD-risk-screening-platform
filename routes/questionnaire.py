"""Questionnaire route.

UI only for now: one question at a time, client-side navigation and
validation. Response storage (questionnaire_responses table) and score
calculation are a separate later milestone -- see CLAUDE.md.
"""

from flask import Blueprint, render_template

questionnaire_bp = Blueprint("questionnaire", __name__)


@questionnaire_bp.route("/questionnaire")
def index():
    return render_template("questionnaire.html")
