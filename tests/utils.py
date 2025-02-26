from django.db import transaction


def force_run_on_commit_functions() -> None:
    db_connection = transaction.get_connection()
    current_run_on_commit = db_connection.run_on_commit
    db_connection.run_on_commit = []
    while current_run_on_commit:
        _, func, _ = current_run_on_commit.pop(0)
        func()
