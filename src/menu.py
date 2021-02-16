import time
import json

import dt_lib

from datetime import datetime

menu = {}

def load_menu():
    global menu
    with open("menu.json", "r", encoding="utf8") as read_file:
        menu = json.load(read_file)

def get_categories():
    categs = []

    for cat in menu:
        categs.append(cat)

    return categs

def get_dishes_for_days(cat, dow, weak_num):
    if menu[cat]:
        dishes = menu[cat]
        today_menu = []

        for dish in dishes:
            for day in dish["days"]:
                if len(day) == 2:
                    if dt_lib.day_of_week(day) == dow:
                        today_menu.append(dish)
                elif len(day) == 4 and day[2] == ':':
                    wom = int(day[3:4])
                    day = day[0:2]
                    if dt_lib.day_of_week(day) == dow and wom == weak_num:
                        today_menu.append(dish)
        return today_menu
    return []


def get_today_menu(category):
    return get_dishes_for_days(category, datetime.now().weekday(), dt_lib.week_of_month(datetime.now()))
