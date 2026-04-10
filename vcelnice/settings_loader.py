import os
from pathlib import Path

from dotenv import load_dotenv


DEFAULT_MANAGE_SETTINGS_MODULE = "vcelnice.settings.development"
DEFAULT_SERVER_SETTINGS_MODULE = "vcelnice.settings.production"
LEGACY_SETTINGS_MODULE = "vcelnice.settings"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEGACY_ENV_PATH = Path.home() / "vcelnice" / ".env"


def load_project_env() -> Path | None:
    for env_path in (PROJECT_ROOT / ".env", LEGACY_ENV_PATH):
        if env_path.is_file():
            load_dotenv(env_path, override=False)
            return env_path
    return None


def normalize_settings_module(
    module_name: str | None,
    default_module: str = DEFAULT_MANAGE_SETTINGS_MODULE,
) -> str:
    if not module_name or module_name == LEGACY_SETTINGS_MODULE:
        return default_module
    return module_name

