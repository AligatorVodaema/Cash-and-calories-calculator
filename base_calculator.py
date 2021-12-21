import datetime as dt
from dataclasses import dataclass
from typing import Union
from config import DATE_FORMAT


class Calculator:

    def __init__(self, limit) -> None:
        self.records = []
        self.limit = limit
        return None
        
    def add_record(self, record) -> None:
        """Add Record instance to internal array."""
        self.records.append(record)
        return None
        
    def get_today_stats(self) -> int:
        """Return sum of record values for the current day.

        Returns:
            [int]: [Sum of record values for the current day]
        """
        current_day = dt.datetime.now().day
        return sum(
            rec.amount for rec in self.records 
            if rec.date.day == current_day
        )
    
    def get_week_stats(self) -> int:
        """Return sum of record values for the last week.

        Returns:
            [int]: [Sum of record values for the last week]
        """
        date_week_ago = dt.datetime.now() - dt.timedelta(days=7)
        return sum(
            rec.amount for rec in self.records if rec.date > date_week_ago
        )
        
    def get_today_amount_remained(self) -> Union[bool, int]:
        """Return available amount if limit not exceeded, otherwise False.

        Returns:
            [bool]: [Return False if the limit is exceeded]
            [int]: [Return the balance if not exceeded]
        """
        total_amount_today = self.get_today_stats()
        if total_amount_today > self.limit:
            return False
        return self.limit - total_amount_today
            


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
        return None
            
        


if __name__ == '__main__':
    r1 = Record(50, 'first', '21.12.2021')
    r2 = Record(1000, 'seconnd')
    
    c = Calculator(1000)
    c.add_record(r1)
    c.add_record(r2)
    print(c.get_today_stats())
    
    
    