from typing import Iterator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from utils.logger import get_logger
from utils.config import BROWSER_NAME, ARTIFACTS_DIR

logger = get_logger(__name__)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    """Hook that generates a report each test for failure handling"""

    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

@pytest.fixture(scope="session", autouse=True)
def artifacts_dirs() -> dict[str, Path]:
    """Directory creation for report files storing"""

    traces_dir = Path(ARTIFACTS_DIR) / "traces"
    screenshots_dir = Path(ARTIFACTS_DIR) / "screenshots"
    traces_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    return {"traces": traces_dir, "screenshots": screenshots_dir}

@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    """Playwright browser creation, type dictated by BROWSER_NAME"""

    with sync_playwright() as pw:
        logger.info(f"Initiating browser session using {BROWSER_NAME}")
        browser = getattr(pw, BROWSER_NAME).launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser, 
            request: pytest.FixtureRequest, 
            artifacts_dirs: dict[str, Path]
            ) -> Iterator[BrowserContext]:
    """Playwright context creation with tracing saved on test fail"""

    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    if request.node.rep_call.failed:
        logger.info(f"Saving trace on failed test {request.node.name}")

        trace_path = artifacts_dirs["traces"] / f"{request.node.name}.zip"
        context.tracing.stop(path=str(trace_path))
        allure.attach.file(
            str(trace_path), 
            name="playwright_trace",
            attachment_type=allure.attachment_type.ZIP,
        )
    else:
        context.tracing.stop()
    
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext, 
         request: pytest.FixtureRequest,
         artifacts_dirs: dict[str, Path]
         ) -> Iterator[Page]:
    """Playwright page creation with screenshot saved on test fail"""

    page = context.new_page()

    yield page

    if request.node.rep_call.failed:
        logger.info(f"Saving screenshot on failed test {request.node.name}")

        screenshot_path = artifacts_dirs["screenshots"] / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(
            str(screenshot_path), 
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    page.close()