import sys
from typing import Tuple, Union

from loguru import logger

from base_calculator import Calculator, Record
from request_currency import (CURRENCY_RATE_URL, CURRENT_DIR,
                              get_current_exchange_rates)

logger.remove()
logger.add(
    CURRENT_DIR + '/logs/records.log',
    level='SUCCESS',
    rotation='24h'
)
logger.add(sys.stdout, level='INFO')
logger.add(CURRENT_DIR +'/logs/ERRORS.log', level='ERROR')


class IncorrectInput(Exception):
    pass


class CaloriesCalculator(Calculator):
    """Calculator for tracking calories.

    Args:
        Calculator ([int]): [calories limit for every day.]
    """
    def get_calories_remained(self) -> str:
        """Generates a response depending on the state of the daily limit."""
        calories_remained, limit_status = self.get_today_amount_remained()
        if limit_status in ('reached', 'exceeded'):
            return "Хватит есть!"
        return ("Сегодня можно съесть ещё, но с общей калорийностью"
                f"не более {calories_remained} кКал."
        )
        
    def get_week_stats(self) -> str:
        """Return received calories for the last week."""
        calories_received = super().get_week_stats()
        return f"За последнюю неделю получено {calories_received} калорий."
    
    def get_today_stats(self) -> str:
        """Return received calories for today."""
        calories_received = super().get_today_stats()
        return f"Сегодня получено {calories_received} калорий."
        
        
class CashCalculator(Calculator):
    """Calculator for tracking spending money.
    
    Args:
        Calculator ([int]): [money limit for every day.]
    """
    CURRENCY_REPRESENTATION = {
            'USD': 'USD',
            'EUR': 'Euro',
            'RUB': 'руб'
    }
    
    def get_today_cash_remained(self, currency: str) -> str:
        """Generates a response depending on the state of the limit.

        Args:
            Currency ([str]) [currency that user will see in representation]
        
        Returns:
            [str]: [information about the status of the limit 
            and the ability to spend.]
        """
        currency_rates = get_current_exchange_rates()
        lower_currency_names = [
            str.lower(cur_name) for cur_name in currency_rates['Valute']
        ]
        if currency not in lower_currency_names:
            raise IncorrectInput(
                "Введите одну из доступных валют: " +
                "/".join(lower_currency_names)
            )
            
        cash_remained, limit_status = self.get_today_amount_remained()
        
        if limit_status == 'reached':
            return "Денег нет, держись."
        elif limit_status == 'exceeded':
            result_message = "Денег нет, держись: твой долг - {} {}."
        else:
            result_message = "На сегодня осталось {} {}."
            
        cash_remained, currency_name = self._convert_currency(
            currency=currency, 
            cash=abs(cash_remained)
        )
        return result_message.format(cash_remained, currency_name)

          
    @classmethod
    def _convert_currency(cls, currency: str, cash: int) -> Tuple[float, str]:
        """Converts money into the desired currency.

        Args:
            currency ([str]) [currency name from user.]
            cash ([int]) [money in default currency.]

        Returns:
            [tuple]: 
                [float]: [converted representation to the desired currency.]
                [str]: [currency name for representation.]
        """
        curr_rates = get_current_exchange_rates()
        if currency == CURRENCY_RATE_URL[1].lower():
            currency_rate = 1
        else:
            currency_rate = curr_rates['Valute'][currency.upper()]['Value']
        
        cash = cls._convert_single_currency(cash, currency_rate)
        
        try:
            currency_name = cls.CURRENCY_REPRESENTATION[currency.upper()]
        except KeyError:
            currency_name = currency.upper()
        
        return (cash, currency_name)
    
    @staticmethod
    def _convert_single_currency(
        cash: Union[int, float],
        rate: Union[int, float]
    ) -> float:
        return round(cash / rate, 2)

    def get_week_stats(self) -> str:
        """Return spended money for the last week."""
        spended_money = super().get_week_stats()
        return (
            f"За последнюю неделю потрачено {spended_money} "
            f"{self.CURRENCY_REPRESENTATION['RUB']}."
        )
        
    def get_today_stats(self) -> str:
        """Return spended money for today."""
        spended_money = super().get_today_stats()
        return (
            f"Сегодня потрачено {spended_money} "
            f"{self.CURRENCY_REPRESENTATION['RUB']}"
        )
        
        
if __name__ == '__main__':
    rec1 = Record(5, 'купил сухарики', '22.12.2021')
    rec2 = Record(100, 'купил певко')
    
    cash_calc = CashCalculator(1000)
    cash_calc.add_record(rec1)
    cash_calc.add_record(rec2)
    print(cash_calc.get_today_cash_remained('eur'))
    print(cash_calc.get_today_cash_remained('amd'))
    print(cash_calc.get_week_stats(), end='\n\n')
    
    rec3 = Record(1000, 'съел еду')
    
    calories_calc = CaloriesCalculator(900)
    calories_calc.add_record(rec3)
    print(calories_calc.get_today_stats())
    print(calories_calc.get_week_stats())
    print(calories_calc.get_calories_remained())
    