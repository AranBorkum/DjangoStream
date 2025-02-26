import pathlib

PROJECT_ROOT = pathlib.Path(__file__, "..").resolve().parent
DJANGO_SETTINGS_MODULE = "project.settings"
PYTHON_PATH = "src/:tests/:PYTHONPATH"
