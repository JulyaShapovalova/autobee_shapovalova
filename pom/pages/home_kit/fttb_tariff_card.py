import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.block import Block
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.page_factory.title import Title
from pom.pages.home_kit.activation_request_popup import ActivationRequestPopup
from pom.pages.home_kit.data import SPECIAL_OFFER_TITLE
from pom.shared_components.tariff_catalogues.tariff_card import TariffCard


class FttbTariffCard(TariffCard):
    def __init__(
            self,
            page: Page,
            parent_locator: Locator,
            tariff_name: str = None,
            alias: str = None,
            index: int = None
    ) -> None:
        super().__init__(page, parent_locator, tariff_name, alias, index, 'home')
        self.page = page
        self.name = tariff_name
        self._base_href = '/customers/products/home/home-tariffs/tariffs/kit/{alias}/'

        self.tariff_title = Title(self.page, self.tariff_link.locator.locator('xpath=.//*[@data-t-id="common-Flex"]/*[@data-component="Text"]'), 'Заголовок тарифа')
        self.activation_button = Button(self.page, self.locator.locator('button'), 'Подключение тарифа')

        self._card_top_container = self.locator.locator('xpath=.//*[contains(@data-t-id,"CardSection") and .//*[@data-t-id="cards-CardBg"]]')
        self._card_bottom_container = self.locator.locator('xpath=.//*[contains(@data-t-id,"CardSection") and .//*[@data-t-id="ui-enhancers"]]')
        self.special_offer_label = Block(self.page, self._card_top_container.locator('[data-component=Tag]'), SPECIAL_OFFER_TITLE)
        self._speed_container = self._card_top_container.locator('[data-t-id=cards-Values]')
        self.speed_values = Description(self.page, self._speed_container.locator('[data-component=Text]'), 'Значение скорости')
        self._spacer_container = self._card_bottom_container.locator('[data-t-id*=Spacer]')
        self.description = Description(self.page, self._spacer_container.locator('xpath=.//preceding-sibling::*'), 'Рекламное описание тарифа')
        self._footer_container = self._spacer_container.locator('xpath=.//following-sibling::*')
        self.price = Description(self.page, self._footer_container.locator('xpath=./*[.//*[contains(text(),"₽")]]'), 'Стоимость интернет-тарифа')

    def activate(self) -> ActivationRequestPopup:
        with allure.step(f'Подключить тариф {self.name}'):
            activation_popup = ActivationRequestPopup(self.page)
            self.activation_button.click_until_element_visible(activation_popup.h2, attempts_limit=3)
            activation_popup.h2.should_have_text('Заявка на подключение')
            activation_popup.subtitle.should_have_text('Адрес и контактный телефон')
            return activation_popup

    def should_have_special_offer(self) -> None:
        with allure.step(f'Проверить: блок "{SPECIAL_OFFER_TITLE}" ({self.name}) имеет верный текст'):
            self.special_offer_label.should_have_text(SPECIAL_OFFER_TITLE)

    def should_have_speed(self, speed: int) -> None:
        value = f'{speed} Мбит/с'
        with allure.step(f'Проверить: скорость интернет-тарифа имеет верное значение – "{value}"'):
            self.speed_values.should_have_all_text_contents(value)

    def should_have_description(self, description: str) -> None:
        with allure.step(f'Проверить: описание интернет-тарифа верное – "{description}"'):
            self.description.should_have_text(description)

    def should_have_price(self, price: int):
        value = f'{price}₽/месяц'
        with allure.step(f'Проверить: стоимость интернет-тарифа имеет верное значение – "{value}"'):
            self.price.should_have_text(value)
