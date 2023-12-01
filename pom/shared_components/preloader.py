from playwright.sync_api import Page, Locator
from pom.page_factory.block import Block
from pom.page_factory.image import Image


class Preloader(Block):
    def __init__(self, page: Page, parent_locator: Locator) -> None:
        super().__init__(page, parent_locator.locator('[data-component=Preloader]'), 'Колёсико загрузки')
        self.page = page
        self.preloader_image = Image(self.page, self.locator.locator('svg'), self.type_of)
