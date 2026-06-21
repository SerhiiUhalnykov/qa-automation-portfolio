from typing import Iterator
from pathlib import Path

import pytest
import allure
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from utils.logger import get_logger
from utils.config import BROWSER_NAME

logger = get_logger(__name__)


@pytest.fixture(autouse=True)
def allure_markings() -> None:
    allure.dynamic.parameter("browser", BROWSER_NAME)
    allure.dynamic.parent_suite(BROWSER_NAME.upper())


@pytest.fixture(scope="session")
def artifacts_subdir() -> str:
    return BROWSER_NAME


@pytest.fixture(scope="session")
def artifact_extensions() -> list[str]:
    return ["zip", "png"]


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    """Playwright browser creation, type dictated by BROWSER_NAME"""

    with sync_playwright() as pw:
        logger.info(f"Initiating browser session using {BROWSER_NAME}")
        browser = getattr(pw, BROWSER_NAME).launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Iterator[BrowserContext]:
    """Playwright context creation with tracing"""

    context = browser.new_context()
    # NOTE: tracing stoppage is handled by the save_attach_results fixture
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Iterator[Page]:
    """Playwright page creation"""

    page = context.new_page()
    yield page
    page.close()


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
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        screenshot_path = artifacts_path["png"]
        trace_path = artifacts_path["zip"]
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
