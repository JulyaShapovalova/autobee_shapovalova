import allure
from playwright.sync_api import Page
from pom.page_factory.tab import Tab
import pom.pages.elk.main.page as elk
from pom.pages.identity_error.page import IdentityErrorPage
from pom.page_factory.image import Image
from pom.page_factory.button import Button
from pom.page_factory.link import Link
from pom.page_factory.input import Input
from pom.page_factory.title import Title
from pom.page_factory.description import Description
from pom.pages.login.data import LOGIN_FORM_TITLE


class LoginForm:
    def __init__(self, page: Page) -> None:
        self.form_name = 'форма логина'
        self.page = page
        self._elk_page = elk.ElkPage

        self._container = self.page.locator('[data-t-id=components-FormContainer]')

        self._header_form = self._container.locator('[data-t-id=components-FormHeader]')
        self.logo = Image(self.page, self._header_form.locator('img'), f'{self.form_name}')
        self.title = Title(self.page, self._header_form.locator('h1'), f'{self.form_name}')

        self._initial_form = self._container.locator('.initial-form')

        self._tabs_form = self._initial_form.locator('[data-component=Tabs]')
        self.tab_by_mobile_id = Tab(self.page, self._tabs_form.locator('xpath=.//*[@data-component="Tab"][.//*[text()="Мобильный ID"]]'), 'Мобильный ID')
        self.tab_by_sms = Tab(self.page, self._tabs_form.locator('xpath=.//*[@data-component="Tab"][.//*[text()="По SMS"]]'), 'По SMS')
        self.tab_by_password = Tab(self.page, self._tabs_form.locator('xpath=.//*[@data-component="Tab"][.//*[text()="С постоянным паролем"]]'), 'С постоянным паролем')

        self._initial_form_content = self._initial_form.locator('.initial-form__tab-content')

        self._mobile_id_initial_form = self._initial_form_content.locator('#MOBILE_ID_INITIAL')
        self.mobile_id_number_description = Description(self.page, self._mobile_id_initial_form.locator('xpath=./*[text()]'), 'Поле ввода (MobID)')
        self.mobile_id_number_input = Input(self.page, self._mobile_id_initial_form.locator('input'), 'Телефон (MobID)')

        self._sms_initial_form = self._initial_form_content.locator('#SMS_INITIAL')
        self.sms_number_description = Description(self.page, self._sms_initial_form.locator('xpath=./*[text()]'), 'Поле ввода (SMS)')
        self.sms_number_input = Input(self.page, self._sms_initial_form.locator('label input'), 'Телефон (SMS)')

        self._constant_pass_initial_form = self._initial_form_content.locator('#PASSWORD')
        self._pass_login_container = self._constant_pass_initial_form.locator('xpath=.//label[./*[@name="login"]]')
        self.pass_login_input = Input(self.page, self._constant_pass_initial_form.locator('[name=login]'), 'Логин')
        self.pass_login_description = Description(self.page, self.pass_login_input.get_locator().locator('xpath=./preceding-sibling::*[text()]'), 'Поле логина')
        self._pass_password_container = self._constant_pass_initial_form.locator('xpath=.//label[./*[@name="password"]]')
        self.pass_password_input = Input(self.page, self._pass_password_container.locator('[name=password]'), 'Пароль')
        self.pass_password_description = Description(self.page, self.pass_password_input.get_locator().locator('xpath=./preceding-sibling::*[text()]'), 'Поле пароля')

        self.forgot_password_link = Link(self.page, self._constant_pass_initial_form.locator('[data-component=Link]'), 'Я не помню пароль')

        self._bottom_form = self._initial_form.locator('xpath=./following-sibling::*')
        self.submit_button = Button(self.page, self._bottom_form.locator('[type=submit]'), 'Подтверждение')

    def auth_by_pass(self, ctn: str, password: str, is_correct=True):
        message = f'Авторизоваться пользователем {ctn} с постоянным паролем "{password}"' if is_correct \
            else f'Авторизоваться пользователем {ctn} с неверным паролем "{password}"'
        with allure.step(message):
            self.tab_by_password.click()
            self.tab_by_password.should_be_selected()
            self.pass_login_description.should_have_text('Введите логин')
            self.pass_password_description.should_have_text('Введите пароль')
            self.submit_button.should_be_disabled()
            self.pass_login_input.fill(ctn)
            self.submit_button.should_be_enabled()
            self.pass_password_input.fill(password)
            self.submit_button.click()
            if is_correct:
                page = elk.ElkPage(self.page)
            else:
                page = IdentityErrorPage(self.page)
            page.should_have_correct_url()
            return page

    def should_have_correct_title(self):
        with allure.step(f'Проверить: заголовок "{self.form_name}" верный – "{LOGIN_FORM_TITLE}"'):
            self.title.should_have_text(LOGIN_FORM_TITLE)

