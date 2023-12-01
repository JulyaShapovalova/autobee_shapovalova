import phonenumbers

RU = 'RU'
CELLPHONE_ID = 1


def mobile_ctn_beautifier(ctn: str, spaces_only=False) -> str:
    phone_number = phonenumbers.parse(ctn, RU)
    if phonenumbers.phonenumberutil.number_type(phone_number) != CELLPHONE_ID:
        raise Exception('Введённый номер не является мобильным номером')
    formatted_phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return formatted_phone_number.replace('-', ' ') if spaces_only else formatted_phone_number
