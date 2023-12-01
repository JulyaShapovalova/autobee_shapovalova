import allure
from lib.fixtures.allure_fixtures import set_allure_info
from lib.helpers.common_helper import data
from pom.pages.home.page import HomePage
from tests.header.data import TestData


@allure.suite('Шапка сайта')
@allure.sub_suite('Выбор региона')
class TestRegionSelection:
    t362 = TestData.T362
    test_data_t362 = data(t362)

    @set_allure_info(t362['test_case']['id'])
    def test_t362_region_with_long_name(
            self,
            home_page: HomePage,
            region=test_data_t362['region'],
            expected=test_data_t362['expected_values']
    ):
        home_page.header.should_have_region_detector_message(expected['region_detection_message'])
        home_page.header.should_have_region_detector_confirmation_button_text(expected['confirm_button_text'])
        home_page.header.should_have_region_detector_rejection_button_text(expected['refuse_button_text'])
        region_list_popup = home_page.header.reject_region()
        region_list_popup.title.should_have_text(expected['popup_title'])
        region_list_popup.close_button.should_be_enabled()
        region_list_popup.select_region(region_name=region['ru'], region_alias=region['en'], entry_page=home_page)
        home_page.header.regions_toggle.should_have_text(region['ru'])
        home_page.should_have_correct_url()
