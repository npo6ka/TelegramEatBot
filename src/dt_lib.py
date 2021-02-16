from datetime import datetime

from math import ceil

week = {
    'Mo': 0,
    'Tu': 1,
    'We': 2,
    'Th': 3,
    'Fr': 4,
    'Sa': 5,
    'Su': 6
}

def day_of_week(day_name):
    if day_name in week:
        return week[day_name]
    else:
        print("Error day_num on day_of_week functions: ", day_name)
        return week[0]

def week_of_month(dt):
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))