import invoke

from tasks import constants


@invoke.task
def run_python_type_checker(ctx):
    """
    Run ruff format against the repository.
    """
    with ctx.cd(str(constants.PROJECT_ROOT)):
        # Print out the version to help with local vs CI debugging
        ctx.run("uv run mypy src tests --strict")
