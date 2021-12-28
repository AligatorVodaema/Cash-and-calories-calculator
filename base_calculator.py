import datetime as dt
from dataclasses import dataclass
from typing import Tuple

from loguru import logger

from request_currency import CURRENT_DIR


DATE_FORMAT = '%d.%m.%Y'
logger.add(
    CURRENT_DIR + '/logs/records_{time}.log',
    level='SUCCESS',
    rotation='24h'
)


class Calculator:
    """Base calculator for tracking values.
    
    Args:
        Calculator ([int]): [value limit for every day.]
    """
    def __init__(self, limit: int) -> None:
        """Save limit value and create list for records.

        Args:
            limit [int]: [simple integer value.]
        """
        self.records = []
        self.limit = limit
        return None
        
    def add_record(self, record: 'Record') -> None:
        """Add Record instance to internal array."""
        self.records.append(record)
        return None
        
    def get_today_stats(self) -> int:
        """Return sum of record values for the current day.

        Returns:
            [int]: [Sum of record values for the current day.]
        """
        current_day = dt.datetime.now().day
        return sum(
            rec.amount for rec in self.records 
            if rec.date.day == current_day
        )
    
    def get_week_stats(self) -> int:
        """Return sum of record values for the last week.

        Returns:
            [int]: [Sum of record values for the last week.]
        """
        date_week_ago = dt.datetime.now() - dt.timedelta(days=7)
        return sum(
            rec.amount for rec in self.records if rec.date > date_week_ago
        )
        
    def get_today_amount_remained(self) -> Tuple[int, str]:
        """Return the difference between the limit and costs, for today.
        And limit status.

        Returns:
            [tuple]: 
                [int]: [the difference between the limit and costs, for today.]
                [str]: [limit reached or not, or exceeded.]
        """
        total_amount_today = Calculator.get_today_stats(self)
        limit_status = 'not reached'
        
        if total_amount_today > self.limit:
            limit_status = 'exceeded'
        elif total_amount_today == self.limit:
            limit_status = 'reached'
        return (self.limit - total_amount_today, limit_status)


@dataclass
class Record:
    amount: int
    comment: str
    date: dt.datetime = dt.datetime.now()
    def __post_init__(self) -> None:
        """Covert to datetime obj from str.
        
        Convert if date passed to instance like string.
        """
        if not isinstance(self.date, dt.datetime):
            self.date = dt.datetime.strptime(self.date, DATE_FORMAT)
        logger.success(f'{self.amount=}, {self.comment=}, {self.date=}')
        return None
            

if __name__ == '__main__':
    rec1 = Record(50, 'first', '21.12.2021')
    rec2 = Record(1000, 'seconnd')
    
    calc = Calculator(1000)
    calc.add_record(rec1)
    calc.add_record(rec2)
    print(calc.get_today_stats())
    