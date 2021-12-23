# Two calculators.
## One to track money spent another to track calories received.<br>
Requirements: Python 3.9

Without user interface.
### Usage Calories Calculator:

1. Create venv and run python<code>$ python(your_version)</code> in directory with project.
2. Import this <code>from base_calculator import CaloriesCalculator, Record</code>.
3. Create CaloriesCalculator instance with the desired daily calorie limit. Like <code>cal_c = CaloriesCalculator(1500)</code>
4. Create some records of what you ate and when <code>rec = Record(1001, 'eat cake')</code> or with a date <code>rec = Record(1001, 'eat cake', '11.11.2021')</code>. 
Date format <code>DD.MM.YYYY</code>.
5. Add some records to your Calculator like this <code>cal_c.add_record(rec)</code>.
6. And now you can use one of these methods: 

#### Generates a response depending on the state of the daily limit.
<code>cal_c.get_today_cash_remained()</code>:

#### Return received calories for the last week.
<code>cal_c.get_week_stats()</code>:

#### Return received calories for today.
<code>cal_c.get_today_stats()</code>:


### Usage Cash Calculator:

1. Create venv and run python<code>$ python(your_version)</code> in directory with project.
2. Import this <code>from base_calculator import CashCalculator, Record</code>.
3. Create CashCalculator instance with the desired daily money limit. Like <code>cash_c = CashCalculator(1000)</code>
4. create some records on what you spent the cash on and when <code>rec = Record(150, 'buy cola')</code> or with a date 
<code>rec = Record(150, 'buy cola', '12.12.2021')</code>. 
Date format <code>DD.MM.YYYY</code>.
5. Add some records to your Calculator like this <code>cash_c.add_record(rec)</code>.
6. And now you can use one of these methods: 

#### Generates a response depending on the state of the daily limit.
<code>cash_c.get_today_cash_remained(currency)</code>

Where "currency" is: 

In what currency do you want to see the result(<code>'rub'</code> or <code>'usd'</code> or <code>'eur'</code> or another...)

#### Return spended money for the last week.
<code>cash_c.get_week_stats()</code>:

#### Return spended money for today.
<code>cash_c.get_today_stats()</code>:
