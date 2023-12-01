from playwright.sync_api import Page
from pom.pages.base_page import BasePage
import pom.shared_components.main_header.header as header
import pom.pages.my_beeline.sidebar as sidebar


class MyBeelineBasePage(BasePage):
    def __init__(self, page: Page, path: str, name: str) -> None:
        super().__init__(page, path=path, name=name)
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)
        self.sidebar = sidebar.SideBar(self.page, self._page_wrapper)
