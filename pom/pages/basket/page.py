from playwright.sync_api import Page
from pom.pages.base_page import BasePage


class BasketPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='/basket/', name="Корзина")
        self.page = page
