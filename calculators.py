from typing import Tuple, Union
from enum import Enum

from base_calculator import Calculator, Record


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
    
    Default currency is Rubles.
    Args:
        Calculator ([int]): [money limit for every day.]
    """
    USD_RATE = 73
    EUR_RATE = 83
    RUB_RATE = 1
    curreency_rates = {
            'usd': (USD_RATE, 'USD'),
            'eur': (EUR_RATE, 'Euro'),
            'rub': (RUB_RATE, 'руб')
    }
    DEFAULT_CURRENCY = curreency_rates['rub']
    
    def get_today_cash_remained(self, currency: str) -> str:
        """Generates a response depending on the state of the limit.

        Args:
            Currency ([str]) [currency that user will see in representation]
        
        Returns:
            [str]: [information about the status of the limit 
            and the ability to spend.]
        """
        if currency not in self.curreency_rates.keys():
            return (
                "Введите одну из доступных валют: " +
                "/".join(self.curreency_rates.keys())
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
        currency_rate, currency_name = cls.curreency_rates[currency]
        cash = cls._convert_single_currency(cash, currency_rate)
        
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
            f"{self.DEFAULT_CURRENCY[-1]}."
        )
        
    def get_today_stats(self) -> str:
        """Return spended money for today."""
        spended_money = super().get_today_stats()
        return (
            f"Сегодня потрачено {spended_money} "
            f"{self.DEFAULT_CURRENCY[-1]}"
        )
        
        
if __name__ == '__main__':
    rec1 = Record(5, 'купил сухарики', '22.12.2021')
    rec2 = Record(100, 'купил певко')
    
    cash_calc = CashCalculator(1000)
    cash_calc.add_record(rec1)
    cash_calc.add_record(rec2)
    print(cash_calc.get_today_cash_remained('QQQ'))
    print(cash_calc.get_today_cash_remained('eur'))
    print(cash_calc.get_today_cash_remained('usd'))
    print(cash_calc.get_week_stats(), end='\n\n')
    
    rec3 = Record(1000, 'съел еду')
    
    calories_calc = CaloriesCalculator(900)
    calories_calc.add_record(rec3)
    print(calories_calc.get_today_stats())
    print(calories_calc.get_week_stats())
    print(calories_calc.get_calories_remained())
    