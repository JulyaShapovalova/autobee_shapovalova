from lib.data.regions import MOSKVA, VORONEZH, KALUGA, VOLGOGRAD


class Users:
    """
    Класс-справочник пользователей.
    """
    NONEXISTENT_USER = {
        'all': {
            'number': '1111111111',
            'password': 'nonexistent_password',
        }
    }

    USER_WITH_INCORRECT_PASSWORD = {
        'prod': {
            'number': '9601648369',
            'password': 'Test3000',
        },
        'prodlike': {
            'number': '9601648369',
            'password': 'Test3000',
        }
    }

    ELK_PAYMENTS_USER = {
        'prod': {
            'number': '9670147551',
            'password': 'Qwerty44$',
        },
        'prodlike': {
            'number': '9670147551',
            'password': 'Qwerty44$',
        },
        'webtest': {
            'number': '9058002001',
            'password': 'Qwerty44'
        }
    }

    USER_AUTH = {
        'prod': {
            'number': '9629849866',
            'password': '88dorogA',
            'bill_type': 'prepaid'
        },
        'prodlike': {
            'number': '9629849866',
            'password': '88dorogA',
            'bill_type': 'prepaid'
        },
        'webtest': {
            'number': '9058002001',
            'password': 'Qwerty44',
            'bill_type': 'prepaid'
        },
    }

    BLOCKED_USER = {
        'prod': {
            'number': '0857885247',
            'password': '123456789Qq'
        },
        'prodlike': {
            'number': '0857885247',
            'password': '123456789Qq'
        },
        'webtest': {
            'number': '0894821775',
            'password': 'Qwerty44'
        }
    }

    MOBILE_POSITIVE = {
        'prod': {
            'number': '9601090743',
            'password': '88dorogA',
            'region': VORONEZH,
        },
        'prodlike': {
            'number': '9601090743',
            'password': '88dorogA',
            'region': VORONEZH,
        },
        'webtest': {
            'number': '9058002307',
            'password': 'Qwerty44',
            'region': VORONEZH,
        }
    }

    SSO_CONNECTION_AVAILABLE_USER = {
        'prod': {
            'number': '9033153039',
            'password': '88dorogA',
        },
        'prodlike': {
            'number': '9033153039',
            'password': '88dorogA',
        },
        'webtest': {
            'number': '9058002201',
            'password': 'Qwerty44'
        },
    }

    SSO_CONNECTED_USER = {
        'prod': {
            'number': '9601090741',
            'password': '88dorogA',
            'region': VORONEZH
        },
        'prodlike': {
            'number': '9601090741',
            'password': '88dorogA',
            'region': VORONEZH
        },
        'webtest': {
            'number': '9058002206',
            'password': 'Qwerty44',
            'region': MOSKVA,
        },
    }

    SSO_PROHIBITED_USER = {
        'prod': {
            'number': '9524586705',
            'password': '88dorogA'
        },
        'prodlike': {
            'number': '9524586705',
            'password': '88dorogA'
        },
        'webtest': {
            'number': '9058002317',
            'password': 'Qwerty44'
        },
    }

    MOBILE_NEGATIVE_BILL_TYPE = {
        'prod': {
            'number': '9641400056',
            'password': '88dorogA',
            'region': KALUGA,
            'bill_type': 'prepaid'
        },
        'prodlike': {
            'number': '9641400056',
            'password': '88dorogA',
            'region': KALUGA,
            'bill_type': 'prepaid'
        },
        'webtest': {
            'number': '9683574039',
            'password': 'Qwerty44',
            'region': KALUGA,
            'bill_type': 'prepaid'
        },
    }

    BROADBAND_USER = {
        'prod': {
            'number': '0850724412',
            'password': '88dorogA',
            'region': VOLGOGRAD,
        },
        'prodlike': {
            'number': '0850724412',
            'password': '88dorogA',
            'region': VOLGOGRAD,
        },
        'webtest': {
            'number': '0894890269',
            'password': 'Qwerty44',
            'region': VOLGOGRAD,
        },
    }

    ANOTHER_OPERATOR_USER = {
        'all_env': {
            'number': '9530262447'
        }
    }
