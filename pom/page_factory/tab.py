import re
from re import Pattern
import allure
from pom.page_factory.base_component import BaseComponent


class Tab(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'вкладка'

    @property
    def default_selected_class(self) -> Pattern:
        return re.compile('tabs__item--selected-secondary')

    def should_be_selected(
            self,
            expected_class: str | list | Pattern = None,
            expected_background_color: str = None,
            expected_border_color: str = None
    ) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" выбрана (активна)'):
            if not expected_class and not expected_background_color and not expected_border_color:
                self.should_have_class(self.default_selected_class, timeout=3000)
            if expected_class:
                self.should_have_class(expected_class, timeout=3000)
            if expected_background_color:
                self.should_have_css_property('background-color', expected_background_color, timeout=3000)
            if expected_border_color:
                self.should_have_css_property('border-color', expected_border_color, timeout=3000)
