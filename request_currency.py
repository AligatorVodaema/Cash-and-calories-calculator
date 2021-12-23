import json
import os
import datetime as dt
import glob
from typing import Dict

import requests

CURRENT_DIR = os.path.dirname(__file__)
CURRENCY_RATE_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def remove_all_json_dumps() -> None:
    """Delete all files in data dir."""
    json_dumps = glob.glob(CURRENT_DIR + '/currency_data/*')
    if json_dumps:
        [os.unlink(json_file) for json_file in json_dumps]
    return None
    

def find_single_json_dump() -> str:
    """Return file name with dump from data dir."""
    return next(
            os.scandir(CURRENT_DIR + '/currency_data')
    ).name


def request_current_currencies() -> None:
    """Request data on exchange rates and save them in json."""
    print('Request sent!')
    response = requests.get(CURRENCY_RATE_URL)
    current_dt = dt.datetime.now()
    with open(
        CURRENT_DIR + f'/currency_data/{current_dt}.json', mode='w'
    ) as f:
        json.dump(response.json(), fp=f, indent=4, ensure_ascii=False)
    return None


def check_last_update_currency() -> None:
    """Update dump if it is out of date.
    
    Or send request for new dump if dump not found.
    """
    # looking for dump.
    try:
        dump_json_file_name = find_single_json_dump()
    except StopIteration:
        # dump not found, create new.
        request_current_currencies()
        return None
        
    # check dump time.
    last_update_time = dump_json_file_name.removesuffix('.json')
    last_update_dt = dt.datetime.fromisoformat(last_update_time)
    hour_ago = dt.datetime.now() - dt.timedelta(hours=1)
    # if more than an hour, update.
    if hour_ago > last_update_dt:
        remove_all_json_dumps()
        request_current_currencies()
    return None

    
def load_rates_from_dump() -> Dict:
    """Request and save dump or read from file.
    
    Return a dict with multiple meanings about exchange rates.
    Can be seen by visiting 'CURRENCY_RATE_URL'.
    """
    try:
        dump_name = find_single_json_dump()
    except StopIteration:
        request_current_currencies()
        dump_name = find_single_json_dump()
        
    with open(CURRENT_DIR + f'/currency_data/{dump_name}', mode='r') as f:
        currency_dict = json.load(fp=f)
    return currency_dict

    
def get_current_exchange_rates() -> Dict:
    """Return a fresh exchange rate."""
    check_last_update_currency()
    return load_rates_from_dump()


if __name__ == '__main__':
   print(get_current_exchange_rates())
   