import re
from typing import List, Pattern
import allure
from playwright.sync_api import Page, Response, Locator
from lib.helpers import url_helper
from lib.helpers.assertion import Assertion as assertion
from lib.helpers.url_helper import get_url_without_query_params
from pom.page_factory.block import Block
from pom.page_factory.button import Button
from pom.page_factory.checkbox import Checkbox
from pom.page_factory.description import Description
from pom.page_factory.image import Image
from pom.page_factory.input import Input
from pom.page_factory.link import Link
from pom.pages.base_page import BasePage
from pom.pages.search.data import SHOW_ALL_LINK_TEXT, HIDE_ALL_LINK_TEXT, RESET_FILTERS_BUTTON_TEXT, MANUFACTURER_TEXT


class SearchPage(BasePage):
    def __init__(self, page: Page, query: str):
        super().__init__(page, path=f'/search/', query_params={'term': query}, name=f'Поиск "{query}"')
        self.page = page
        self.__query = query
        self._queries_order = ['term', 'price', 'filters']

        self._sidebar_container = self._page_wrapper.locator('aside')

        self._filters_mapper_container = self._sidebar_container.locator('[data-t-id*=FiltersMapper]')
        self._filter_wrapper_container = self._filters_mapper_container.locator('[data-t-id*=FilterWrapper]')
        self._filter_names = self._filter_wrapper_container.locator('xpath=./*[@data-name]')

        self._filter_label_container = self._sidebar_container.locator('[data-t-id*=FilterLabel]')
        self.filter_counter = Block(self.page, self._filter_label_container.locator('[data-component=Counter]'), 'Счётчик фильтров')
        self.reset_filters_link = Link(self.page, self._filter_label_container.locator('a'), RESET_FILTERS_BUTTON_TEXT)

        self._filter_price_container = self._sidebar_container.locator('xpath=./*[contains(@data-t-id,"FilterWrapper")]')
        self._price_container = self._filter_price_container.filter(has_text='Цена')
        self.min_price_input = Input(self.page, self._price_container.locator('#min'), 'Минимальная цена')
        self.max_price_input = Input(self.page, self._price_container.locator('#max'), 'Максимальная цена')

        self._manufacturers_container = self._filter_wrapper_container.filter(has_text=MANUFACTURER_TEXT)
        self.manufacturers_cell_button = Button(self.page, self._manufacturers_container.locator('[type=button]'), MANUFACTURER_TEXT)
        self.manufacturers_content_container = self.manufacturers_cell_button.locator.locator('xpath=./following-sibling::*')
        self._manufacturer_container = self.manufacturers_content_container.locator('[data-component=Checkbox]')
        self.show_manufacturers_link = Link(self.page, self.manufacturers_content_container.get_by_text(SHOW_ALL_LINK_TEXT), SHOW_ALL_LINK_TEXT)
        self.hide_manufacturers_link = Link(self.page, self.manufacturers_content_container.get_by_text(HIDE_ALL_LINK_TEXT), HIDE_ALL_LINK_TEXT)

        self._search_result_container = self._sidebar_container.locator('xpath=./following-sibling::*')
        self.total_hits = Description(self.page, self._search_result_container.locator('[data-t-id*=TotalHits]'), 'Найдено товаров')

    @property
    def manufacturers_content_block(self) -> Block:
        return Block(self.page, self.manufacturers_content_container, MANUFACTURER_TEXT)

    def __add_price_filter_query_params(self, price: int) -> None:
        self._query_params['price'] = f'{price};{self.get_max_price()}'
        self._query_params = {key: self._query_params[key] for key in self._queries_order if key in self._query_params}
        self._page_url = url_helper.join_url(self.base_url, self._path, self._query_params)

    def __remove_brand_filter_query_params(self) -> None:
        selected_filters = self.get_selected_manufacturer_filters()
        if len(selected_filters) == 0:
            self._query_params.pop('filters')
        else:
            parts = self._query_params['filters'].split(':')
            brands = parts[1].split(';')
            filtered_brands = [brand for brand in brands if brand in selected_filters]
            updated_brands = f'{parts[0]}:{";".join(filtered_brands)}'
            self._query_params['filters'] = updated_brands
        self._page_url = url_helper.join_url(self.base_url, self._path, self._query_params)

    def __append_brand_filter_query_params(self, manufacture_name: str) -> None:
        if self._query_params.get('filters'):
            self._query_params['filters'] += f';{manufacture_name}'
        else:
            self._query_params['filters'] = f'brands:{manufacture_name}'
            self._query_params = {key: self._query_params[key] for key in self._queries_order if key in self._query_params}
        self._page_url = url_helper.join_url(self.base_url, self._path, self._query_params)

    def get_filter_count(self) -> int:
        with allure.step('Получить: количество применённых фильтров'):
            return int(self.filter_counter.get_text())

    def reset_filters(self, response_url_pattern: str | Pattern = None) -> None | Response:
        # TODO:
        #  по мере добавления тестов на фильтры других блоков (кроме цены и производителей),
        #  добавить нужные проверки, модифицировав метод
        with allure.step(RESET_FILTERS_BUTTON_TEXT):
            action = self.reset_filters_link.click
            if response_url_pattern:
                response = self.wait_for_response(response_url_pattern, action)
            else:
                action()
                response = None
            self._query_params = {'term': self.__query}
            self._page_url = url_helper.join_url(self.base_url, self._path, self._query_params)
            self.should_have_correct_url()
            return response

    def get_response_main_categories(self, response: Response) -> List[str]:
        with allure.step(f'Получить: основной список фильтров, возвращённый в методе {get_url_without_query_params(response.url)}'):
            return ['Производитель' if category['name'] == 'brands' else category['name'] for category in response.json()['facets']][2::]

    def get_main_categories(self) -> List[Locator]:
        with allure.step('Получить: список основных категорий фильтров'):
            return [element.text_content() for element in self._filter_names.all()]

    def get_min_price(self) -> int:
        with allure.step('Получить значение минимальной цены'):
            return int(self.min_price_input.get_attribute('placeholder'))

    def get_max_price(self) -> int:
        with allure.step('Получить значение максимальной цены'):
            return int(self.max_price_input.get_attribute('placeholder'))

    def set_min_price(self, price: int, response_url_pattern: str | Pattern) -> None | Response:
        with allure.step(f'Установить минимальную цену: {price} рублей'):
            response = self.wait_for_response(response_url_pattern, self.min_price_input.fill, value=str(price))
            # # self.page.wait_for_load_state('load')
            self.__add_price_filter_query_params(price)
            self.__remove_brand_filter_query_params()
            self.should_have_correct_url()
            return response

    def get_response_manufacturers(self, response: Response) -> List[dict]:
        with allure.step(f'Получить: список фильтров производителей, возвращённый в методе {get_url_without_query_params(response.url)}'):
            return [facet['values'] for facet in response.json()['facets'] if facet['name'] == 'brands'][0]

    def get_response_selected_manufacture_filters(self, response: Response) -> List[dict]:
        message_url = {get_url_without_query_params(response.url)}
        with allure.step(f'Получить: список выбранных фильтров производителей, возвращённый в методе {message_url} в структуре selectedFacets'):
            selected_facet_values = [
                facet['values'] for facet in response.json()['selectedFacets'] if facet['name'] == 'brands'
            ]
            if len(selected_facet_values) > 0:
                return selected_facet_values[0]
            else:
                return []

    def get_selected_manufacturer_filters(self) -> List[str]:
        with allure.step('Получить: список выбранных фильтров производителей'):
            return [manufacturer.text_content() for manufacturer in self._manufacturer_container.all() if manufacturer.is_checked()]

    def get_manufacturers_and_values(self):
        with allure.step('Получить: список фильтров производителей'):
            manufacturers = []
            for elem in self._manufacturer_container.all():
                manufacturers.append(
                    {
                        'id': elem.text_content(),
                        'name': elem.text_content(),
                        'value': int(elem.locator('xpath=./following-sibling::*[@data-component="Text"]').text_content())
                    }
                )
            return manufacturers

    def show_all_manufacturers(self) -> None:
        with allure.step(f'Раскрыть список фильтров всех производителей'):
            self.show_manufacturers_link.click()
            self.show_manufacturers_link.should_not_be_visible()
            self.hide_manufacturers_link.should_be_visible()

    def check_manufacturer_filter(self, manufacturer_name: str, response_url_pattern: str | Pattern = None) -> None | Response:
        with allure.step(f'Выбрать фильтр производителя "{manufacturer_name}"'):
            manufacturer_link = Link(self.page, self._manufacturer_container.filter(has_text=manufacturer_name), manufacturer_name)
            checkbox_image = Image(self.page, manufacturer_link.locator.locator('[clip-rule]'), 'Чекбокс производителя')
            checkbox_image.should_have_attribute('clip-rule', 'evenodd')
            action = manufacturer_link.click
            if response_url_pattern:
                response = self.wait_for_response(response_url_pattern, action)
            else:
                action()
                response = None
            checkbox_image.should_have_attribute('clip-rule', 'nonzero')
            # self.page.wait_for_load_state('load')
            self.__append_brand_filter_query_params(manufacturer_name)
            self.should_have_correct_url()
            return response

    def uncheck_manufacturer_filter(self, manufacturer_name: str, response_url_pattern: str | Pattern = None) -> None | Response:
        with allure.step(f'Убрать фильтр производителя "{manufacturer_name}"'):
            manufacturer_link = Link(self.page, self._manufacturer_container.filter(has_text=manufacturer_name), manufacturer_name)
            checkbox_image = Image(self.page, manufacturer_link.locator.locator('[clip-rule]'), 'Чекбокс производителя')
            checkbox_image.should_have_attribute('clip-rule', 'nonzero')
            action = manufacturer_link.click
            if response_url_pattern:
                response = self.wait_for_response(response_url_pattern, action)
            else:
                action()
                response = None
            checkbox_image.should_have_attribute('clip-rule', 'evenodd')
            # self.page.wait_for_load_state('load')
            self.__remove_brand_filter_query_params()
            self.should_have_correct_url()
            return response


    def get_total_hits(self) -> int:
        with allure.step('Получить: значение найденных товаров'):
            message = self.total_hits.get_text()
            match = re.search(r'\b\d+\b', message)
            if match:
                number = int(match.group())
                return number
            else:
                raise Exception(f'Число в сообщении "{message}" не найдено')

    def should_have_main_filter_categories(self, response: Response) -> None:
        with allure.step(f'Проверить: основной список фильтров, возвращённый в методе {get_url_without_query_params(response.url)}, верный'):
            page_filter_names = self.get_main_categories()
            response_filter_names = self.get_response_main_categories(response)
            assertion.equal(page_filter_names, response_filter_names, 'Фильтры поиска')

    def should_have_manufacturers_and_values(self, response: Response) -> None:
        with allure.step(f'Проверить: список фильтров производителей и значения количества товаров, возвращённый в методе {get_url_without_query_params(response.url)}, верный'):
            sorted_response_manufacturers = sorted(self.get_response_manufacturers(response), key=lambda d: d['name'])
            sorted_page_manufacturers = sorted(self.get_manufacturers_and_values(), key=lambda d: d['name'])
            assertion.equal(sorted_page_manufacturers, sorted_response_manufacturers, 'Фильтры производителей')

    def should_have_selected_manufacturer_filters(self, manufacturers: List[dict], response: Response) -> None:
        with allure.step(f'Проверить: список выбранных фильтров производителей, возвращённый в методе {get_url_without_query_params(response.url)}, верный'):
            # sorted_manufactures = sorted(manufacturers, key=lambda d: d['name'])
            # sorted_response_manufactures = sorted(self.get_response_selected_manufacture_filters(response), key=lambda d: d['name'])
            # assertion.equal(sorted_response_manufactures, sorted_manufactures, 'Выбранные фильтры производителей')
            sorted_manufactures = [manufacturer['name'] for manufacturer in manufacturers]
            sorted_manufactures.sort()
            sorted_response_manufactures = [manufacturer['name'] for manufacturer in self.get_response_selected_manufacture_filters(response)]
            sorted_response_manufactures.sort()
            assertion.equal(sorted_response_manufactures, sorted_manufactures, 'Выбранные фильтры производителей')

    def should_not_display_manufacturer(self, manufacturer: str) -> None:
        with allure.step(f'Проверить: фильтр производителя "{manufacturer}" отсутствует в списке'):
            Checkbox(
                self.page,
                self._manufacturer_container.filter(has_text=manufacturer),
                f'Производитель "{manufacturer}"'
            ).should_not_be_visible()

    def should_have_hits_count(self, expected: int) -> None:
        with allure.step(f'Проверить: общее число результатов поиска – {expected}'):
            assertion.equal(self.get_total_hits(), expected, 'Количество результатов поиска')
