import os
from re import Pattern
import lib.helpers.url_helper as url_helper
from abc import abstractmethod
import allure
from playwright.sync_api import expect, Page, Response
from pom.page_factory.block import Block
from pom.page_factory.title import Title
from pom.shared_components.preloader import Preloader


class BasePage:
    def __init__(self, page: Page, base_url='', path='', query_params: dict[str, ...] | None = None, name=''):
        self.name = name
        self.page = page
        self.base_url = base_url if base_url else os.getenv('BASE_URL')
        self._path = path
        self._query_params = query_params
        self._page_url = url_helper.join_url(self.base_url, self._path, self._query_params)

        self._main_wrapper = self.page.locator('.react-adaptive-wrapper')
        self._page_wrapper = self.page.locator('.react-adaptive-page')
        self._main_content = self._page_wrapper.locator('.main-content')

        self.h1 = Title(self.page, self._page_wrapper.locator('h1'), 'Заголовок (h1)')

        self.preloader = Preloader(self.page, self._main_wrapper)
        self.skeleton = Block(self.page, self._main_wrapper.locator('[data-component=Skeleton]'), 'Незагруженная пустышка')

    @property
    @abstractmethod
    def type_of(self) -> str:
        return 'страница'

    def set_region_by_url(self, region_name: str) -> None:
        current_region = url_helper.get_region(self.base_url)
        os.environ['BASE_URL'] = self.base_url.replace(current_region, region_name)
        self._page_url = self._page_url.replace(current_region, region_name)

    def visit(self, url=None) -> None:
        full_url = url if url else self._page_url
        with allure.step(f'Открыть: {full_url}'):
            self.page.goto(full_url, wait_until='domcontentloaded')

    def back(self) -> None:
        with allure.step('Перейти назад'):
            self.page.go_back()

    def forward(self) -> None:
        with allure.step('Перейти вперёд'):
            self.page.go_forward()

    def reload(self) -> None:
        with allure.step('Обновить страницу'):
            self.page.reload()

    def take_screenshot(self) -> bytes:
        return self.page.screenshot()

    def get_current_url(self) -> str:
        return self.page.url

    def get_path(self) -> str:
        return self._path

    def get_query_params(self) -> dict[str, ...]:
        return self._query_params

    def get_cookies(self):
        return self.page.context.cookies(self.get_current_url())

    def get_cookie(self, cookie) -> str:
        return list(filter(lambda c: c['name'] == cookie, self.page.context.cookies(self.get_current_url())))[0]['value']

    def wait_for_full_load(self, timeout: int = None) -> None:
        with allure.step('Ожидание: запросы выполнены, контент загружен'):
            self.page.wait_for_load_state('load')
            self.preloader.should_not_be_visible(timeout=timeout)
            self.skeleton.should_not_be_visible(timeout=timeout)

    def wait_for_response(self, url_pattern:  str | Pattern, action, **kwargs) -> Response:
        with allure.step(f'Ожидание: запрос "{url_pattern}" выполнен во время действия {action.__name__}'):
            with self.page.expect_response(url_pattern) as response_info:
                action(**kwargs)
            return response_info.value

    def should_have_correct_url(self) -> None:
        """
        Функция проверки URL на соответствие его "вшитому" ожидаемому результату – _page_url
        :return:
        """
        with allure.step(f'Проверить: {self.type_of} "{self.name}" открыта – адрес в браузере верный: {self._page_url}'):
            expect(self.page).to_have_url(self._page_url)

    def should_have_url(self, url: str) -> None:
        """
        Функция проверки URL на соответствие ожидаемому URL, переданному в качестве аргумента
        :param url: ожидаемый URL
        :return:
        """
        with allure.step(f'Проверить: {self.type_of} "{self.name}" имеет верный URL: {url}'):
            expect(self.page).to_have_url(url)

    def should_have_title(self, title: str | Pattern[str]) -> None:
        with allure.step(f'Проверить: заголовок вкладки верный – "{title}"'):
            expect(self.page).to_have_title(title)
