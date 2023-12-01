import allure
from playwright.sync_api import expect
from pom.page_factory.base_component import BaseComponent


class Description(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'описание'
