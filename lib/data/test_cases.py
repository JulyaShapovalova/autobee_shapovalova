from allure_commons.types import Severity
from lib.data.owners import Owners

HEADER_TEST_CASES = {
    'T362': {
        'title': 'Выбор другого региона/города с длинным названием при первичном заходе в НЗ',
        'id': 'T362',
        'severity': Severity.NORMAL,
        'owner': Owners.BEELINOV,
    },
}

ALL_TEST_CASES = (
    HEADER_TEST_CASES,
)
