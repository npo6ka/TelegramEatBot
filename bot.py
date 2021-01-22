import telebot
import config
import notificator
import threading
import time
import traceback

from telebot import types

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

@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('static/homer_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id,
        "Приветсвую тебя, {0.first_name}!\n <b>{1.first_name}</b>,"
        " бот созданный чтоб накормить тебя, если повезёт.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=create_markup(message.chat.id))


@bot.message_handler(content_types=['text'])
def msg_back(message):
    if message.chat.type == 'private':
        if message.text == 'Текущий список еды':
            bot.send_message(message.chat.id, "Это информация сейчас тебе не нужна")
        elif message.text == 'Заказать еды':
            bot.send_message(message.chat.id, "Мне кажется ты слишком много жрёшь")
        elif message.text == 'Подписаться на уведомления':
            if not notificator.is_sub_exist(message.chat.id):
                notificator.add_to_subs(message.chat.id)
                bot.send_message(message.chat.id, "Ты успешно добавлен в подпизжиков",
                    reply_markup=create_markup(message.chat.id))
            else:
                bot.send_message(message.chat.id, "Зачем тебя ещё раз добавлять?",
                    reply_markup=create_markup(message.chat.id))
        elif message.text == 'Отписаться от уведомлений':
            if notificator.is_sub_exist(message.chat.id):
                notificator.remove_subs(message.chat.id)
                bot.send_message(message.chat.id, "Ты успешно удалён из подпизжиков",
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
            