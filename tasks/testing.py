import invoke

from tasks import constants


@invoke.task
def run_tests(ctx, *, nature: str = "unit"):
    assert nature.lower() in constants.TestOption
    with ctx.cd(str(constants.PROJECT_ROOT)):
        if nature == constants.TestOption.ALL.value:
            ctx.run(
                f"DJANGO_SETTINGS_MODULE={constants.DJANGO_SETTINGS_MODULE} "
                f"PYTHONPATH={constants.PYTHON_PATH} "
                f"uv run pytest tests"
            )
        else:
            ctx.run(
                f"DJANGO_SETTINGS_MODULE={constants.DJANGO_SETTINGS_MODULE} "
                f"PYTHONPATH={constants.PYTHON_PATH} "
                f"uv run pytest tests/{nature}"
            )
