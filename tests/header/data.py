from lib.data.regions import TAIMYRSKY_REGION
from lib.data.test_cases import HEADER_TEST_CASES as TC
from pom.shared_components.main_header.data import ARE_YOU_IN_MOSCOW, CONFIRM_REGION_BUTTON_TEXT, \
    REJECT_REGION_BUTTON_TEXT, REGION_LIST_POPUP_TITLE


class TestData:
    T362 = {
        'test_case': TC['T362'],
        'data': {
            'prod': {
                'region': TAIMYRSKY_REGION,
                'expected_values': {
                    'region_detection_message': ARE_YOU_IN_MOSCOW,
                    'confirm_button_text': CONFIRM_REGION_BUTTON_TEXT,
                    'refuse_button_text': REJECT_REGION_BUTTON_TEXT,
                    'popup_title': REGION_LIST_POPUP_TITLE,
                }
            },
            'prodlike': {
                'region': TAIMYRSKY_REGION,
                'expected_values': {
                    'region_detection_message': ARE_YOU_IN_MOSCOW,
                    'confirm_button_text': CONFIRM_REGION_BUTTON_TEXT,
                    'refuse_button_text': REJECT_REGION_BUTTON_TEXT,
                    'popup_title': REGION_LIST_POPUP_TITLE,
                }
            }
        }
    }
