"""Flask application entry point.

Phase 5 skeleton only: app factory + homepage. No database, consent,
questionnaire, or cognitive-task routes yet -- see CLAUDE.md and
docs/ADHD_Project_Master_Specification.md §30 for the milestone order.
"""

import os

from flask import Flask

from config import config


def create_app(config_name=None):
    """Application factory."""
    app = Flask(__name__)

    config_name = config_name or os.environ.get("FLASK_CONFIG", "default")
    app.config.from_object(config[config_name])

    from routes.main import main_bp

    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
