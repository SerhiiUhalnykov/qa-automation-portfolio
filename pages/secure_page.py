import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage

class SecurePage(BasePage):
    PATH: str = "/secure"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self._logout_btn = self._page.get_by_role("link", name="Logout")
        self._success_popup = self._page.locator("#flash")

    @allure.step("Check secure page is loaded")
    def is_loaded(self) -> None:
        
        heading = self._page.get_by_role("heading", name="Secure Area", exact=True)

        expect(heading).to_be_visible()
        expect(self._logout_btn).to_be_visible()
    
    @allure.step("Check the success popup visibility")
    def check_success_popup(self) -> None:
        
        expect(self._success_popup).to_contain_text("You logged into a secure area")
        expect(self._success_popup).to_be_visible()

    @allure.step("Perform logout")
    def logout(self) -> None:

        self._logout_btn.click()