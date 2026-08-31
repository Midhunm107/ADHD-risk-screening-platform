"""Flask configuration.

Single source of truth for app settings, mirroring how
adhd_ml_pipeline/configs/config.yaml centralizes the ML pipeline's config.
Nothing here talks to a database yet -- that's added in a later Phase 5
milestone once models/ exists.
"""

import os


class Config:
    """Base configuration shared by all environments."""

    # Placeholder for local development only. Must be overridden via the
    # SECRET_KEY environment variable before any real deployment.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key")

    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}
