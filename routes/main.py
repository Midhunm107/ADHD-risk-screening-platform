"""Homepage route.

Only the homepage exists so far. Consent, questionnaire, and cognitive-task
routes are separate future milestones (see CLAUDE.md).
"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/consent")
def consent():
    return render_template("consent.html")
