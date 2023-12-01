import os


def data(test_case):
    """
    Функция получения тестовых данных (пользователь, тариф, адрес, другие данные, ожидаемые значения и прочее)
    в зависимости от окружения, на котором запускаются тесты.

    :param test_case: Словарь вида: T1993 = {'test_case': test_case, 'data': {'prod': {'user': Users.PROD['UserOne']}}}
    :return: Словарь с данными (например, значение T1993['data']['prod'] для случая, когда запускаются тесты на прод)
    """
    env = os.getenv('ENV_NAME')
    try:
        if env == 'uat':
            env = 'prodlike'
        return test_case['data'][env]
    except:
        return test_case['data']['all_env']


def str_to_bool(value: str) -> bool:
    if type(value) is str:
        return value.lower() in ('yes', 'true', 't', '1')
    else:
        raise ValueError(f'Переданное значение {str(value)} не является строкой')
