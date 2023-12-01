from typing import Pattern
import allure
from playwright.sync_api import Page, Locator, Response
import pom.pages.login.page as login
from pom.page_factory.block import Block
from pom.page_factory.description import Description
from pom.page_factory.image import Image
from pom.page_factory.button import Button
from pom.page_factory.input import Input
from pom.pages.base_page import BasePage
from pom.pages.search.page import SearchPage
from pom.shared_components.main_header.data import *
from pom.shared_components.main_header.expanded_menu import ExpandedMenu
from pom.shared_components.main_header.region_list_popup import RegionListPopup


class MainHeader(Block):
    def __init__(self, page: BasePage, parent_locator: Locator) -> None:
        super().__init__(page.page, parent_locator.locator('.desktopOnlyElement'), 'Шапка сайта')
        self.page_instance = page
        self.page = page.page
        self._parent_locator = parent_locator
        self._expanded_menu = ExpandedMenu(self.page, self.locator)

        self._top_header_container = self.locator.locator('xpath=.//*[@id="toggleButton-regions-desktop"]/parent::*/parent::*')

        self.regions_toggle = Button(self.page, self._top_header_container.locator('#toggleButton-regions-desktop'), 'Смена региона')
        self._region_auto_detector_container = self.regions_toggle.locator.locator('xpath=./parent::*/following-sibling::*[.//*[@type="button"]]')
        self.region_auto_detector_message = Description(self.page, self._region_auto_detector_container.locator('p'), ARE_YOU_IN_MOSCOW)
        self.region_auto_detector_confirm_button = Button(self.page, self._region_auto_detector_container.locator('xpath=.//button[./*[contains(text(),"Да")]]'), CONFIRM_REGION_BUTTON_TEXT)
        self.region_auto_detector_reject_button = Button(self.page, self._region_auto_detector_container.locator('xpath=.//button[./*[contains(text(),"Нет")]]'), REJECT_REGION_BUTTON_TEXT)

        self._bottom_header_container = self._top_header_container.locator('xpath=./following-sibling::*')

        self._menu_container = self._bottom_header_container.locator('xpath=./*[.//img]')
        self.logo = Image(self.page, self._menu_container.locator('img'), 'Логотип')

        self.catalogue_button = Button(self.page, self._menu_container.locator('button span'), 'Каталог')

        self._search_form_container = self._bottom_header_container.locator('#searchForm')
        self.search_input = Input(self.page, self._search_form_container.locator('#search_open_modal'), 'Поиск')
        self.search_button = Button(self.page, self._bottom_header_container.locator('[form=searchForm]'), 'Найти')

        self.personal_button = Button(self.page, self._bottom_header_container.locator('.personal a'), 'Войти')

    def reject_region(self) -> RegionListPopup:
        with allure.step('Нажать: отказ от предложенного региона'):
            self.region_auto_detector_reject_button.click()
            dialog_container = self.page.get_by_role('dialog')
            return RegionListPopup(self.page, dialog_container)

    def change_region(self, region_name: str, search_by_input: bool = False, region_alias: str = None) -> Page:
        message = f'Изменить регион, выбрав из списка "{region_name}'"" if not search_by_input \
            else f'Изменить регион на "{region_name}", воспользовавшись формой поиска'
        with allure.step(message):
            dialog_container = self.page.get_by_role('dialog')
            region_selection_popup = RegionListPopup(self.page, dialog_container)
            self.regions_toggle.click()
            region_selection_popup.title.should_have_text('Выбор региона')
            if search_by_input:
                page = region_selection_popup.search_region(region_name)
            else:
                page = region_selection_popup.select_region(region_name, region_alias, self.page_instance)
            return page

    def catalogue_click(self) -> ExpandedMenu:
        with allure.step('Раскрыть: меню каталога'):
            self.catalogue_button.click_until_element_visible(self._expanded_menu.mobile_button, 3)
            return self._expanded_menu

    def search_click(self, response_url_pattern: str | Pattern = None) -> None | Response:
        action = self.search_input.click
        if response_url_pattern:
            response = self.page_instance.wait_for_response(response_url_pattern, action)
        else:
            action()
            response = None
        self.page_instance.should_have_correct_url()
        return response

    def search(self, query: str, click: bool = True, response_url_pattern: str | Pattern = None) -> (
            tuple[SearchPage, Response] | SearchPage
    ):
        """
        Функция поиска на сайте. Возвращает страницу поиска нужного запроса. Включает в себя необязательный
        параметр "response_url_pattern", передав который, можно включить перехват ответа нужного запроса.
        :param query:
        :param click:
        :param response_url_pattern:
        :return:
        """
        with allure.step(f'Найти: "{query}"'):
            self.search_input.fill(query)
            action = self.search_button.click if click else self.search_input.press_enter
            if response_url_pattern:
                response = self.page_instance.wait_for_response(response_url_pattern, action)
            else:
                action()
            search_page = SearchPage(self.page, query)
            search_page.should_have_correct_url()
            return search_page if not response_url_pattern else (search_page, response)

    def personal_button_click(self) -> login.LoginPage:
        self.personal_button.click()
        login_page = login.LoginPage(self.page)
        login_page.should_have_correct_url()
        login_page.login_form.title.should_be_visible()
        return login_page

    def should_have_region_detector_message(self, expected: str) -> None:
        with allure.step(f'Проверить: сообщение об определении региона верное – "{expected}"'):
            self.region_auto_detector_message.should_have_text(expected)

    def should_have_region_detector_confirmation_button_text(self, expected: str) -> None:
        with allure.step(f'Проверить: текст кнопки подтверждения региона верный – "{expected}"'):
            self.region_auto_detector_confirm_button.should_have_text(expected)

    def should_have_region_detector_rejection_button_text(self, expected: str) -> None:
        with allure.step(f'Проверить: текст кнопки отклонения региона верный – "{expected}"'):
            self.region_auto_detector_reject_button.should_have_text(expected)
