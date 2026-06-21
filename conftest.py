from pathlib import Path

import pytest

from utils.logger import get_logger
from utils.config import ARTIFACTS_DIR

logger = get_logger(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    """Hook that generates a report status each test for failure handling"""

    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(scope="module")
def artifacts_dir(artifacts_subdir: str) -> Path:
    """Create a directory to store test artifacts"""

    art_dir = Path(ARTIFACTS_DIR) / artifacts_subdir
    art_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Artifacts dir: {art_dir}")

    return art_dir


@pytest.fixture(scope="function")
def artifacts_path(
    artifacts_dir: Path,
    artifact_extensions: list[str],
    request: pytest.FixtureRequest,
) -> dict[str, Path]:
    """Create names and paths for test artifacts"""

    logger.info(f"Create filenames under dir: {artifacts_dir}")

    name = request.node.name
    return {
        ext: artifacts_dir / f"{name}.{ext}" for ext in artifact_extensions
    }
