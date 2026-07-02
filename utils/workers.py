import os


def get_worker_id() -> str:
    """Return the current xdist worker ID, or 'main' for non-parallel runs."""

    return os.getenv("PYTEST_XDIST_WORKER", "main")
