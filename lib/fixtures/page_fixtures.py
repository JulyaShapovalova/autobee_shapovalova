import os
import pytest
from playwright.sync_api import Page, BrowserContext
import pom.pages.elk.main.page as elk
from pom.pages.home_kit.page import HomeKitPage
from pom.pages.home.page import HomePage
from pom.pages.identity_error.page import IdentityErrorPage
from pom.pages.login.page import LoginPage
from pom.pages.my_beeline.settings.number_management.page import NumberManagementPage
from pom.pages.service_mobile.page import ServiceMobilePage
from pom.pages.services_catalogue.page import ServicesCataloguePage
from pom.pages.tariff_mobile.page import TariffMobilePage
from pom.pages.tariffs_mobile_catalogue.page import TariffsMobileCatalogue


@pytest.fixture
def page(context: BrowserContext) -> None:
    page = context.new_page()
    source_url = os.getenv('BASE_URL')
    yield page
    os.environ['BASE_URL'] = source_url
    page.close()


@pytest.fixture(scope='function')
def home_page(page: Page) -> HomePage:
    _page = HomePage(page)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def login_page(page: Page) -> LoginPage:
    _page = LoginPage(page)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def identity_error_page(page: Page, signin=None) -> IdentityErrorPage:
    _page = IdentityErrorPage(page, signin=signin)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def home_kit_page(page: Page) -> HomeKitPage:
    _page = HomeKitPage(page)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def elk_page(page: Page) -> elk.ElkPage:
    _page = elk.ElkPage(page)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def number_management_page(page: Page) -> NumberManagementPage:
    _page = NumberManagementPage(page)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def services_catalogue_page(page: Page) -> ServicesCataloguePage:
    _page = ServicesCataloguePage(page)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def service_mobile_page(name: str, alias: str, page: Page) -> ServiceMobilePage:
    _page = ServiceMobilePage(page, name=name, alias=alias)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def tariffs_mobile_catalogue(page: Page) -> TariffsMobileCatalogue:
    _page = TariffsMobileCatalogue(page)
    _page.visit()
    return _page


@pytest.fixture(scope='function')
def tariff_mobile_page(tariff_name: str, alias: str, page: Page) -> TariffMobilePage:
    _page = TariffMobilePage(page, tariff_name, alias)
    _page.visit()
    return _page
