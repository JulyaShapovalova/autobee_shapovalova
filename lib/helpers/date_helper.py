import datetime
from dateutil import relativedelta
import locale


class DateHelper:
    @staticmethod
    def get_current_date(locale_name="ru_RU") -> datetime.date:
        locale.setlocale(locale.LC_ALL, locale_name)
        return datetime.date.today()

    @staticmethod
    def date_plus_n_moths(date: datetime, months: int) -> datetime.date:
        return date + relativedelta.relativedelta(months=months)

    @staticmethod
    def get_month_short_name(date: datetime.date) -> str:
        short_name = date.strftime("%b")
        if short_name == 'сен':
            short_name = 'сент'
        elif short_name == 'ноя':
            short_name = 'нояб'
        return short_name
