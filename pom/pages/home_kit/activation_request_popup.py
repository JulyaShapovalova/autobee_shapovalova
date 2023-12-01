import allure
from lib.helpers.date_helper import DateHelper
from playwright.sync_api import Page, Locator
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.page_factory.image import Image
from pom.page_factory.input import Input
from pom.page_factory.link import Link
from pom.page_factory.title import Title
from pom.pages.home_kit.data import CONNECTION_AVAILABILITY_SUCCESSFUL_MESSAGE, SELECTED_DATE_COLOR
from pom.shared_components.modal import Modal


class ActivationRequestPopup(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Заявка на подключение', parent_locator)
        self.page = page

        self._header_container = self._container.locator('[data-t-id*=ContentHeader]')
        self.subtitle = Title(self.page, self._header_container.locator('h3'), 'Подзаголовок попапа')
        self.success_image = Image(self.page, self._header_container.locator('img[src*="cat_success"]'), 'Котик с пальцем вверх (успех)')
        self.success_subtitle = Title(self.page, self._header_container.locator('h2'), 'Успешная заявка')

        self._address_container = self._container.locator('[data-t-id*=AddressRequestInputsSection]')

        self._street_container = self._address_container.locator(
            'xpath=.//*[normalize-space()="Улица" and @data-component="Text"]/following-sibling::*')
        self.street_input = Input(self.page, self._street_container.locator('input'), 'Улица')
        self.street_selection = Button(self.page, self._street_container.locator('button'), 'Вариант улицы')

        self._building_container = self._address_container.locator(
            'xpath=.//*[normalize-space()="Дом" and @data-component="Text"]/following-sibling::*')
        self.building_input = Input(self.page, self._building_container.locator('input'), 'Дом')
        self.building_selection = Button(self.page, self._building_container.locator('button'), 'Вариант дома')

        self._flat_container = self._address_container.locator(
            'xpath=.//*[normalize-space()="Квартира" and @data-component="Text"]/following-sibling::*')
        self.flat_input = Input(self.page, self._flat_container.locator('input'), 'Квартира')

        self._phone_container = self._container.locator('[data-t-id*=PhoneInputSection]')
        self._phone_input_container = self._phone_container.locator('[data-component=PhoneInput]')
        self.phone_warning_message = Description(
            self.page,
            self._phone_input_container.locator('xpath=.//*[text()]'),
            'Предупреждающее сообщение')
        self.phone_input = Input(self.page, self._phone_input_container.locator('[name=phone]'), 'Контактный номер')

        self._notification_container = self._container.locator('[data-t-id*=ConnectionNotification]')
        self.notification_description = Description(
            self.page,
            self._notification_container.locator('[data-component=Text]'),
            'Возможность подключения')

        self._tariff_title_container = self._container.locator('[data-t-id=common-TariffTitle]')
        self.tariff_and_hardware_link = Link(
            self.page,
            self._tariff_title_container.locator('[data-component=Link]'),
            'Название тарифа')

        self._address_editing_container = self._container.locator('[data-t-id*=BackToTheAddressStep]')
        self.address_editing_description = Description(
            self.page,
            self._address_editing_container.locator('xpath=.//h3[./following-sibling::button]'),
            "Адрес подключения при выборе даты и времени")

        self._calendar_title_container = self._container.locator('[data-t-id*=CalendarTitle]')
        self.calendar_subtitle = Title(
            self.page,
            self._calendar_title_container.locator('h3'),
            'Календарь для выбора даты подключения')

        self._calendar_selection_container = self._container.locator('[data-t-id=CalendarForm-DateSelection]')

        self._time_selection_container = self._calendar_selection_container.locator('[data-t-id*=TimePicker]')
        self.calendar_open_selection_button = Button(
            self.page,
            self._time_selection_container.locator('button'),
            'Выбор доступного времени')
        self.calendar_select_option_button = Button(
            self.page,
            self._time_selection_container.locator('ul button'),
            'Выбор доступного варианта времени')

        self._date_selection_container = self._time_selection_container.locator('xpath=./preceding-sibling::*')
        self._month_date_container = self._date_selection_container.locator('xpath=.//*[./*[text()="1"]]')
        self.month_date_button = Button(self.page, self._month_date_container.locator('xpath=./*'), 'Число месяца')

        self._installer_date_container = self._container.locator('[data-t-id*=SelectedInstallerDate]')
        self.installer_date_subtitle = Title(self.page, self._installer_date_container.locator('h4'), 'Специалист будет...')
        self.installer_date_value = Description(
            self.page,
            self.installer_date_subtitle.get_locator().locator('xpath=./following-sibling::*[@data-component="Text"]').nth(0),
            'Дата и время прибытия специалиста')

        self._bottom_container = self._container.locator('xpath=./ul')
        self.submit_button = Button(self.page, self._bottom_container.locator('button'), 'Далее')
        self._submit_button_preloader = self.submit_button.get_locator().locator('[data-component=Preloader]')

    def select_street(self, street: str) -> None:
        with allure.step(f'Заполнить улицу: {street}'):
            self.street_input.fill(street)
            self.street_selection.nth(1).click()
            self.building_input.should_be_enabled()

    def select_building(self, building: str) -> None:
        with allure.step(f'Заполнить дом: {building}'):
            self.building_input.fill(building)
            self.building_selection.nth(1).click()
            self.flat_input.should_be_enabled()

    def select_flat(self, flat: int) -> None:
        with allure.step(f'Заполнить квартиру: {str(flat)}'):
            self.flat_input.fill(str(flat))

    def fill_contacts(self, ctn: str, is_address_correct: bool = True) -> None:
        message = f'Заполнить номер телефона: {ctn} (адрес корректный)' if is_address_correct \
            else f'Заполнить номер телефона: {ctn} (адрес некорректный)'
        with allure.step(message):
            self.phone_input.fill(ctn)
            if is_address_correct:
                self.submit_button.should_be_enabled()
            else:
                self.submit_button.should_be_disabled()

    def fill_address_and_contacts(self, street: str, building: str, flat: int, ctn: str) -> None:
        """
        Метод для заполнения адреса и контактного номера. Только для позитивных сценариев, когда мы уверены в том,
        что адрес существует и подключение по нему доступно.
        :param street: Улица
        :param building: Дом
        :param flat: Номер квартиры
        :param ctn: Номер телефона
        :return:
        """
        with allure.step('Заполнить адрес и телефон'):
            self.building_input.should_be_disabled()
            self.flat_input.should_be_disabled()
            self.submit_button.should_be_disabled()
            self.select_street(street)
            self.flat_input.should_be_disabled()
            self.select_building(building)
            self.select_flat(flat)
            self.fill_contacts(ctn)
            self.notification_description.should_have_text(CONNECTION_AVAILABILITY_SUCCESSFUL_MESSAGE)

    def select_first_available_time(self) -> None:
        with allure.step('Выбрать первое доступное время'):
            self.calendar_open_selection_button.click()
            self.calendar_select_option_button.nth(0).click()
            self.installer_date_subtitle.should_be_visible()

    def get_selected_available_time(self) -> str:
        with allure.step('Получить значение выбранного доступного времени'):
            return self._time_selection_container.text_content()

    def get_active_day_from_calendar(self) -> str:
        with allure.step('Получить дату, предвыбранную на календаре'):
            date_elements = self.month_date_button.get_locator().all()
            selected_date_elements = list(filter(lambda x: Button(
                self.page, x, f'Кнопка даты: {x.text_content()}'
            ).get_value_of_css_property('background-color') == SELECTED_DATE_COLOR, date_elements))
            if selected_date_elements:
                return selected_date_elements[0].text_content()
            else:
                raise Exception('Ни одна дата не выбрана, либо цвет активного выбора неверный!')

    def should_have_correct_installer_date(self):
        with allure.step('Проверить: дата и время, выбранные в календаре, соответствуют сообщению'):
            today = DateHelper.get_current_date()
            next_month_date = DateHelper.date_plus_n_moths(today, 1)
            installer_actual_day = int(self.get_active_day_from_calendar())
            installer_actual_time = self.get_selected_available_time().replace('-', 'до')
            installer_expected_date = today if installer_actual_day >= today.day else next_month_date
            month_short_name = DateHelper.get_month_short_name(installer_expected_date)
            formatted_installer_actual_day = str(installer_actual_day) if installer_actual_day > 9 else str(f'0{installer_actual_day}')
            expected_message = f'{formatted_installer_actual_day} {month_short_name}. {installer_expected_date.year}, в период с {installer_actual_time}'
            self.installer_date_value.should_have_text(expected_message)

    def should_have_correct_success_final_data(self, success_title: str):
        with allure.step('Проверить: данные на экране успеха корректные'):
            self.success_image.should_be_visible()
            self.success_subtitle.should_have_text(success_title)
