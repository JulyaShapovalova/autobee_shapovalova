from playwright.sync_api import Page, Locator
from pom.pages.base_page import BasePage
from pom.shared_components.main_header.header import MainHeader


class AuthorizedHeader(MainHeader):
    def __init__(self, page: BasePage, parent_locator: Locator) -> None:
        super().__init__(page, parent_locator)
        self.page = page
