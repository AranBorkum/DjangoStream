import invoke

from tasks import constants


@invoke.task
def run_python_formatter(ctx, diff: bool = False):
    """
    Run ruff format against the repository.
    """
    with ctx.cd(str(constants.PROJECT_ROOT)):
        # Print out the version to help with local vs CI debugging
        ctx.run("ruff --version")
        diff_arg = ""
        if diff:
            diff_arg = "--diff"
        ctx.run(f"ruff format {diff_arg}", pty=True, echo=True)


@invoke.task
def run_python_ruff_linter(ctx, *, fix: bool = False):
    """
    Run ruff checks against the repository
    """
    cmd = "ruff"

    # Print out the version to help with local vs CI debugging
    ctx.run(f"{cmd} --version")

    cmd += " check"
    if fix:
        cmd += " --fix"

    with ctx.cd(constants.PROJECT_ROOT):
        ctx.run(f"{cmd} .", pty=True)
