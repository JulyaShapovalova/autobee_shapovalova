import allure
from playwright.sync_api import Page, expect
from lib.helpers import url_helper
from pom.pages.base_page import BasePage
import pom.pages.login.login_form as login_form


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='/login/', name='Логин')
        self.page = page
        self.login_form = login_form.LoginForm(self.page)

    def should_have_correct_url(self, path: str = None) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" открыта – адрес в браузере верный: {self._page_url}'):
            if not path:
                super().should_have_correct_url()
            else:
                pattern = url_helper.join_url(self.base_url, self.get_path(), None) + f"?returnUrl={path}?connect=true"
                expect(self.page).to_have_url(pattern)
