import enum
import pathlib

PROJECT_ROOT = pathlib.Path(__file__, "..").resolve().parent
DJANGO_SETTINGS_MODULE = "project.settings"
PYTHON_PATH = "src/:tests/:PYTHONPATH"


class TestOption(enum.StrEnum):
    UNIT = "unit"
    INTEGRATION = "integration"
    ALL = "all"
