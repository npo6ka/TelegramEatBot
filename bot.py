import telebot
import threading
import time
import traceback

import config
import notificator
import menu
import log

from log import out
from telebot import types
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN, threaded=False)

# keyboard
def create_markup(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Текущий список еды')
    item2 = types.KeyboardButton('Заказать еды')
    item3 = None

    if not notificator.is_sub_exist(user_id):
        item3 = types.KeyboardButton('Подписаться на уведомления')
    else:
        item3 = types.KeyboardButton('Отписаться от уведомлений')
    markup.add(item1, item2, item3)

    return markup

def create_categories_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    categories = menu.get_categories()

    for cat in categories:
        markup.add(types.InlineKeyboardButton(cat, callback_data='type:categories,cat:{0}'.format(cat)))

    return markup

def create_dish_markup(category):
    markup = types.InlineKeyboardMarkup(row_width=1)
    today_menu = menu.get_today_menu(category)

    for i, dish in enumerate(today_menu):
        markup.add(types.InlineKeyboardButton(dish['name'], callback_data='type:dish,cat:{0},id:{1}'.format(category, i)))

    return markup

def parse_callback_data(data):
    if data and isinstance(data, str):
        ret_struct = {}
        strs = data.split(',')
        for rule in strs:
            if rule:
                kv = rule.split(':')
                if len(kv) == 2 and not kv[0] in ret_struct:
                    ret_struct[kv[0]] = kv[1]
        return ret_struct


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            out("User {0} pressed inline button with data: {1}".format(call.message.chat.id, call.data))
            data = parse_callback_data(call.data)

            if 'type' in data and data["type"] == 'categories':
                if 'cat' in data:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                        text=data["cat"], reply_markup=create_dish_markup(data["cat"]))
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Error handling data")
            if 'type' in data and data["type"] == 'dish':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                if 'id' in data and 'cat' in data:
                    dish = menu.get_today_menu(data["cat"])[int(data["id"])]
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=dish["name"])
                    print(dish)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Error handling data")

    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['start'])
def welcome(message):
    out("User {0}, {1} joined to bot".format(message.chat.id, message.from_user.first_name))
    sticker = open('static/isp_hello_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id,
        "Приветсвую тебя, {0.first_name}!\n <b>{1.first_name}</b>,"
        " бот созданный чтоб накормить тебя, если повезёт.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=create_markup(message.chat.id))


@bot.message_handler(content_types=['text'])
def msg_back(message):
    if message.chat.type == 'private':
        out("User {0} send {1}".format(message.chat.id, message.text))
        if message.text == 'Текущий список еды':
            bot.send_message(message.chat.id, "Это информация сейчас тебе не нужна")
        elif message.text == 'Заказать еды':
            bot.send_message(message.chat.id, "Выбери категорию:", reply_markup=create_categories_markup())
        elif message.text == 'Подписаться на уведомления':
            if not notificator.is_sub_exist(message.chat.id):
                notificator.add_to_subs(message.chat.id)
                bot.send_message(message.chat.id, "Успешно добавлен в подписку",
                    reply_markup=create_markup(message.chat.id))
            else:
                bot.send_message(message.chat.id, "Зачем тебя ещё раз добавлять?",
                    reply_markup=create_markup(message.chat.id))
        elif message.text == 'Отписаться от уведомлений':
            if notificator.is_sub_exist(message.chat.id):
                notificator.remove_subs(message.chat.id)
                bot.send_message(message.chat.id, "Успешно удалён из подписки",
                    reply_markup=create_markup(message.chat.id))
            else:
                bot.send_message(message.chat.id, "Тебя же нет в подписчиках",
                    reply_markup=create_markup(message.chat.id))
        else:
            bot.send_message(message.chat.id, "Хз что тебе ответить, на твоё \"{0}\"".format(message.text),
                parse_mode='html')


if __name__ == "__main__":
    # Запускаем проверку времени в отдельном потоке
    x = threading.Thread(target=notificator.check_send_messages, args=())
    x.start()

    # инициализируем меню
    menu.load_menu()
    log.create_log()

    # а это включение бота на прием сообщений
    # обернуто в try, потому что если Telegram сервер станет недоступен, возможен крэш
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            # print("except on Main thread\n")
            print(e)
            # traceback.print_exc()
            # повторяем через 15 секунд в случае недоступности сервера Telegram
            time.sleep(15)
