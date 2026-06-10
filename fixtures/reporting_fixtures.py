from typing import Iterator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import BrowserContext, Page

from utils.logger import get_logger
from utils.config import BROWSER_NAME, ARTIFACTS_DIR

logger = get_logger(__name__)


@pytest.fixture(autouse=True)
def allure_browser_label() -> None:
    allure.dynamic.parameter("browser", BROWSER_NAME)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    """Hook that generates a report status each test for failure handling"""

    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(scope="session", autouse=True)
def artifacts_dir() -> Path:
    """Create a directory to store test artifacts"""

    art_dir = Path(ARTIFACTS_DIR) / BROWSER_NAME
    art_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Artifacts dir: {art_dir}")

    return art_dir


@pytest.fixture(scope="function")
def artifacts_path(
    artifacts_dir: Path, request: pytest.FixtureRequest
) -> dict[str, Path]:
    """Create names and paths for test artifacts"""

    trace_path = artifacts_dir / (request.node.name + ".zip")
    screenshot_path = artifacts_dir / (request.node.name + ".png")

    return {"trace": trace_path, "screenshot": screenshot_path}


@pytest.fixture(autouse=True)
def save_attach_results(
    page: Page,
    context: BrowserContext,
    request: pytest.FixtureRequest,
    artifacts_path: dict[str, Path],
) -> Iterator[None]:
    """Save test artifacts on fail and attach them to Allure report.

    Args:
        page (Page): Playwright page object for screenshot capture;
        context (BrowserContext): Playwright context object for tracing;
        request (FixtureRequest): pytest request object for test status;
        artifacts_path (dict[str, Path]): artifacts files path.
    """

    yield
    # NOTE: the fixture controls test context object tracing stoppage
    # since stopping tracing and saving the file cannot be separated.
    if request.node.rep_call.failed:
        screenshot_path = artifacts_path["screenshot"]
        trace_path = artifacts_path["trace"]
        logger.info(
            "Saving artifacts on failed test: "
            f"{screenshot_path.name}, {trace_path.name}"
        )

        page.screenshot(path=str(screenshot_path), full_page=True)
        context.tracing.stop(path=str(trace_path))

        allure.attach.file(
            str(screenshot_path),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach.file(
            str(trace_path),
            name="playwright_trace",
            attachment_type=allure.attachment_type.ZIP,
        )
    else:
        context.tracing.stop()
