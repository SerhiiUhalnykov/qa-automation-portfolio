from typing import Iterator, Any
from pathlib import Path

import pytest
import allure
from playwright.sync_api import Browser, BrowserContext, Page

from utils.logger import get_logger
from utils.config import settings
from utils.workers import get_worker_id

logger = get_logger(__name__)


@pytest.fixture(autouse=True)
def allure_markings(browser: Browser) -> None:
    """Tag each test with the browser parent suite and xdist worker."""

    name = browser.browser_type.name
    allure.dynamic.parent_suite(name.upper())
    allure.dynamic.parameter("worker", get_worker_id(), excluded=True)


@pytest.fixture(scope="session")
def artifacts_subdir(browser: Browser) -> str:
    """Return the live browser name as the UI artifacts subdirectory."""

    return browser.browser_type.name


def pytest_configure(config: pytest.Config) -> None:
    """Seed the pytest-playwright --browser option from settings.browser.

    Keeps .env's BROWSER authoritative when no --browser is passed on the CLI;
    an explicit --browser (one or more) always takes precedence.
    """

    if not config.option.browser:
        config.option.browser = [settings.browser]


@pytest.fixture(scope="function")
def context(
    browser: Browser, browser_context_args: dict[str, Any]
) -> Iterator[BrowserContext]:
    """Playwright context creation with tracing."""

    context = browser.new_context(**browser_context_args)
    # NOTE: tracing stoppage is handled by the save_attach_results fixture
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Iterator[Page]:
    """Playwright page creation."""

    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(autouse=True)
def save_attach_results(
    page: Page,
    context: BrowserContext,
    request: pytest.FixtureRequest,
    artifacts_path: Path,
) -> Iterator[None]:
    """Save test artifacts on fail and attach them to Allure report.

    Args:
        page (Page): Playwright page object for screenshot capture;
        context (BrowserContext): Playwright context object for tracing;
        request (FixtureRequest): pytest request object for test status;
        artifacts_path (Path): a path for artifact files.
    """

    yield
    # NOTE: the fixture controls test context object tracing stoppage
    # since stopping tracing and saving the file cannot be separated.
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        screenshot_path = Path(f"{artifacts_path}.png")
        trace_path = Path(f"{artifacts_path}.zip")
        logger.info(
            "Saving artifacts on failed test: "
            f"{screenshot_path.name}, {trace_path.name}"
        )

        page.screenshot(path=screenshot_path, full_page=True)
        context.tracing.stop(path=trace_path)

        allure.attach.file(
            screenshot_path,
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach.file(
            trace_path,
            name="playwright_trace",
            attachment_type=allure.attachment_type.ZIP,
        )
    else:
        context.tracing.stop()
