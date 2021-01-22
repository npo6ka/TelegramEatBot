import time
import json

menu = {}

def load_menu(loc_menu):
    with open("menu.json", "r", encoding="utf8") as read_file:
        loc_menu = json.load(read_file)
    
    return loc_menu

def get_categories():
    categs = []

    for cat in menu:
        categs.append(cat)

    return categs

def get_dishes_for_days(cat, day_of_week):
    dishes = menu[cat]
    today_menu = []

    for dish in dishes:
        for day in dish["days"]:
            if day == day_of_week:
                today_menu.append(dish)

    return today_menu


menu = load_menu(menu)
categories = get_categories()

for cat in categories:
    print("\n", cat)
    dishes = get_dishes_for_days(cat, "Mo")
    for dish in dishes:
        print(dish["name"], dish["cost"])