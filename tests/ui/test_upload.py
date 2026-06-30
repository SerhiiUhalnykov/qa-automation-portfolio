import pytest
import allure
from playwright.sync_api import Page
from faker import Faker

from pages.upload_page import UploadPage

fake = Faker()


@allure.feature("Upload")
@allure.story("Uploading files behavior")
@pytest.mark.regression
class TestUpload:
    def test_upload_file_valid(self, page: Page) -> None:

        upload_page = UploadPage(page)
        upload_page.open()
        upload_page.assert_loaded()

        name, content = fake.word(), fake.text()
        upload_page.choose_inmemory_file(name, content)
        upload_page.upload_file()
        upload_page.assert_file_uploaded(name)

    def test_upload_file_empty(self, page: Page) -> None:

        upload_page = UploadPage(page)
        upload_page.open()
        upload_page.assert_loaded()

        upload_page.upload_file()
        upload_page.assert_upload_failed()
