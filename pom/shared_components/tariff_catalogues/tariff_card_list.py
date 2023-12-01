import re
import typing
from typing import List
import allure
from lib.helpers.assertion import Assertion as assertion
from pom.page_factory.block import Block
from pom.pages.base_page import BasePage
from pom.pages.home_kit.fttb_tariff_card import FttbTariffCard
from pom.pages.tariffs_mobile_catalogue.mobile_tariff_card import MobileTariffCard


class TariffCardList(Block):
    def __init__(
            self,
            page: BasePage,
            block: Block,
            tariff_type: typing.Optional[typing.Literal['mobile', 'home']] = 'mobile',
    ):
        super().__init__(page.page, block.locator, f'Список карточек тарифов "{block.name}"')
        self.page = page
        self._block = block
        self._tariff_card = MobileTariffCard if tariff_type == 'mobile' else FttbTariffCard

    @property
    def cards(self) -> List[MobileTariffCard | FttbTariffCard]:
        with allure.step(f'Получить список карточек тарифов в блоке "{self._block.name}"'):
            self.page.wait_for_full_load()
            card_locators = self._block.locator.locator('xpath=.//*[./a[.//*[text()] and not(@data-component)]]')
            cards = []
            for i in range(card_locators.count()):
                cards.append(self._tariff_card(self.page.page, self._block.locator, index=i))
            return cards

    def get_tariff_card_by_full_info(self, tariff_name: str, alias: str) -> MobileTariffCard | FttbTariffCard:
        with allure.step(f'Получить карточку тарифа "{tariff_name}" ({alias}) блока "{self._block.name}"'):
            return self._tariff_card(self.page.page, parent_locator=self._block.locator, tariff_name=tariff_name, alias=alias)

    def get_tariff_card_by_name(self, tariff_name: str) -> MobileTariffCard | FttbTariffCard:
        with allure.step(f'Получить карточку тарифа "{tariff_name}" блока "{self._block.name}"'):
            return self._tariff_card(self.page.page, parent_locator=self._block.locator, tariff_name=tariff_name)

    def get_tariff_card_by_alias(self, alias: str) -> MobileTariffCard | FttbTariffCard:
        with allure.step(f'Получить карточку тарифа "{alias}" блока "{self._block.name}"'):
            return self._tariff_card(self.page.page, parent_locator=self._block.locator, alias=alias)

    def get_tariff_card_by_index(self, index: int) -> MobileTariffCard | FttbTariffCard:
        with allure.step(f'Получить карточку "{index}" тарифа блока "{self._block.name}"'):
            return self._tariff_card(self.page.page, parent_locator=self._block.locator, index=index)

    @property
    def cards_count(self) -> int:
        return len(self.cards)

    def should_have_count_equal(self, count: int) -> None:
        assertion.equal(self.cards_count, count, f'Количество карточек тарифов блока "{self._block.name}"')

    def should_have_count_greater_than(self, count: int) -> None:
        assertion.greater_than(self.cards_count, count, f'Количество карточек тарифов блока "{self._block.name}"')

    def should_have_count_greater_than_or_equal(self, count: int) -> None:
        assertion.greater_than_or_equal(self.cards_count, count, f'Количество карточек тарифов блока "{self._block.name}"')

    def should_contain_aliases(self, alias_list: List[str]):
        with allure.step(f'Проверить: карточки тарифов имеют элиасы в ссылках: {str(alias_list)}'):
            for card in self.cards:
                alias = card.get_alias()
                assertion.to_be_true(any(al in alias for al in alias_list), f'Значение элиаса {alias} корректно')

    def should_contain_up_aliases(self):
        with allure.step(f'Проверить: карточки тарифов имеют элиасы up1-up5'):
            card_aliases = [card.get_alias() for card in self.cards]
            pattern = re.compile(r'up(\d)')
            found_numbers = {int(pattern.search(item).group(1)) for item in card_aliases if pattern.search(item)}
            assertion.to_be_true(set(range(1, 6)).issubset(found_numbers), 'Карточки содержат элиасы up от 1 до 5')
