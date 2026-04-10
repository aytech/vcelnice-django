from importlib import import_module
import os

from vcelnice.settings_loader import (
    DEFAULT_MANAGE_SETTINGS_MODULE,
    normalize_settings_module,
)

_active_module_name = normalize_settings_module(
    os.environ.get("DJANGO_SETTINGS_MODULE"),
    default_module=DEFAULT_MANAGE_SETTINGS_MODULE,
)
_active_module = import_module(_active_module_name)

for _name in dir(_active_module):
    if _name.isupper():
        globals()[_name] = getattr(_active_module, _name)

__all__ = [name for name in globals() if name.isupper()]
