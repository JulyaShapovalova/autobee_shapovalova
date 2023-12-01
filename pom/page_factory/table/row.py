from pom.page_factory.base_component import BaseComponent


class TableRow(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'строка таблицы'