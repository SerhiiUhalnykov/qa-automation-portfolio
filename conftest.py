from typing import Iterator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from utils.logger import get_logger
from utils.config import BROWSER_NAME

logger = get_logger(__name__)

pytest_plugins = [
    "fixtures.reporting_fixtures",
]


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
