import telebot
import config
import time
import json
import traceback

from datetime import datetime
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
notify_subs = []

def save_subs():
    with open("subs.json", "w") as write_file:
        json.dump(notify_subs, write_file)

def load_subs():
    with open("subs.json", "r") as read_file:
        subs = json.load(read_file)
        for sub in subs:
            notify_subs.append(sub)
        print("loaded subscribers: ", notify_subs)

def is_food_time(hour, min):
    now = datetime.now()
    is_weekend = now.weekday() >= 5
    cur_hour = int(now.strftime("%H"))
    cur_min = int(now.strftime("%M"))

    return cur_hour == hour and cur_min == min and not is_weekend

def is_sub_exist(id):
    return id in notify_subs

def add_to_subs(id):
    if not is_sub_exist(id):
        notify_subs.append(id)
        print("Added new subs: ", id)
        save_subs()

def remove_subs(id):
    for i, sub in enumerate(notify_subs):
        if id == sub:
            notify_subs.pop(i)
            print("Removed from subs: ", id)
            save_subs()
            return

# это функция отправки сообщений по времени
def check_send_messages():
    load_subs()

    # флаг проверки чтобы сообщение не выводилось дважды
    notify_flag = True

    while True:
        try:
            if is_food_time(config.NOTIFICATION_TIME_HOUR, config.NOTIFICATION_TIME_MIN):
                if notify_flag:
                    print("ВРЕМЯ писать еду!!!")
                    for sub in notify_subs:
                        bot.send_message(sub, "Пора писать еду !!!")
                    notify_flag = False
            else:
                notify_flag = True
            # пауза между проверками, чтобы не загружать процессор
            time.sleep(59)
        except Exception as e:
            print("except on child thread\n")
            print(e)
            traceback.print_exc()