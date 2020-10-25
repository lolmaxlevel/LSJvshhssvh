# -*- coding: utf-8 -*-
import requests
import json
import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import schedule
import time
import threading
from geopy.geocoders import Nominatim
import difflib
import news.govno
import image.image
import random
from PIL import Image, ImageDraw, ImageFont

token = '1229958568:AAEBxq5OwU3lS8mXax6kIu7eQ1wBd8ak15Y'  # bot constants
bot = telebot.TeleBot(token)

users = {}  # constants for db
with open('users.txt') as json_file:
    users = json.load(json_file)
    print(users.keys())

REGIONS = {'111': 'европа', '166': 'СНГ', '318': 'Универсальное', '183': 'Азия', '225': 'Россия',
           '17': 'Северо-Западный федеральный округ', '10857': 'Калининградская область', '22': 'Калининград',
           '10897': 'Мурманская область', '23': 'Мурманск', '10933': 'Республика Карелия', '18': 'Петрозаводск',
           '2': 'Санкт-Петербург', '10926': 'Псковская область', '25': 'Псков', '10928': 'Великие Луки',
           '10904': 'Новгородская область', '24': 'Великий Новгород', '3': 'Центральный федеральный округ',
           '10819': 'Тверская область', '14': 'Тверь', '10795': 'Смоленская область', '12': 'Смоленск',
           '10650': 'Брянская область', '191': 'Брянск', '10693': 'Калужская область', '6': 'Калуга', '967': 'Обнинск',
           '10705': 'Курская область', '8': 'Курск', '10772': 'Орловская область', '10': 'Орёл',
           '10832': 'Тульская область', '15': 'Тула', '213': 'Москва', '214': 'Долгопрудный', '215': 'Дубна',
           '216': 'Зеленоград', '217': 'Пущино', '10645': 'Белгородская область', '4': 'Белгород',
           '10712': 'Липецкая область', '9': 'Липецк', '10841': 'Ярославская область', '16': 'Ярославль',
           '10658': 'Владимирская область', '192': 'Владимир', '10656': 'Александров', '10661': 'Гусь-Хрустальный',
           '10668': 'Муром', '10687': 'Ивановская область', '5': 'Иваново', '10776': 'Рязанская область',
           '11': 'Рязань', '10802': 'Тамбовская область', '13': 'Тамбов', '10672': 'Воронежская область',
           '193': 'Воронеж', '26': 'Южный федеральный округ', '11029': 'Ростовская область', '39': 'Ростов-на-Дону',
           '11053': 'Шахты', '971': 'Таганрог', '238': 'Новочеркасск', '11036': 'Волгодонск',
           '10995': 'Краснодарский край', '35': 'Краснодар', '1107': 'Анапа', '970': 'Новороссийск', '239': 'Сочи',
           '1058': 'Туапсе', '10990': 'Геленджик', '10987': 'Армавир', '10993': 'Ейск', '11004': 'Республика Адыгея',
           '1093': 'Майкоп', '11020': 'Карачаево-Черкесская республика', '1104': 'Черкесск',
           '11013': 'Кабардино-Балкарская республика', '30': 'Нальчик', '11021': 'Северная Осетия', '33': 'Владикавказ',
           '11012': 'Республика Ингушетия', '11024': 'Чеченская республика', '1106': 'Чечня',
           '11010': 'Республика Дагестан', '28': 'Махачкала', '11069': 'Ставропольский край', '36': 'Ставрополь',
           '11043': 'Каменск-Шахтинский', '11067': 'Пятигорск', '11063': 'Минеральные Воды', '11057': 'Ессентуки',
           '11062': 'Кисловодск', '11015': 'Республика Калмыкия', '1094': 'Элиста', '10946': 'Астраханская область',
           '37': 'Астрахань', '10950': 'Волгоградская область', '38': 'Волгоград',
           '40': 'Приволжский федеральный округ', '11146': 'Поволжье', '194': 'Саратов', '11132': 'Жигулевск',
           '11143': 'Балаково', '11095': 'Пензенская область', '49': 'Пенза', '11117': 'Республика Мордовия',
           '42': 'Саранск', '11153': 'Ульяновская область', '195': 'Ульяновск', '11131': 'Самарская область',
           '51': 'Самара', '240': 'Тольятти', '11139': 'Сызрань', '11156': 'Чувашская республика', '45': 'Чебоксары',
           '11077': 'Республика Марий Эл', '41': 'Йошкар-Ола', '11079': 'Нижегородская область',
           '47': 'Нижний Новгород', '11083': 'Саров', '11070': 'Кировская область', '46': 'Киров',
           '10699': 'Костромская область', '7': 'Кострома', '10853': 'Вологодская область', '21': 'Вологда',
           '10842': 'Архангельская область', '20': 'Архангельск', '10849': 'Северодвинск',
           '10176': 'Ненецкий автономный округ', '10939': 'Республика Коми', '19': 'Сыктывкар',
           '11148': 'Удмуртская республика', '44': 'Ижевск', '11119': 'Республика Татарстан', '43': 'Казань',
           '236': 'Набережные Челны', '11127': 'Нижнекамск', '11108': 'Пермский край', '50': 'Пермь',
           '11111': 'Республика Башкортостан', '172': 'Уфа', '11114': 'Нефтекамск', '11115': 'Салават',
           '11116': 'Стерлитамак', '11084': 'Оренбургская область', '48': 'Оренбург', '972': 'Дзержинск',
           '52': 'Уральский федеральный округ', '11225': '(Урал)  Челябинская область', '56': 'Челябинск',
           '235': 'Магнитогорск', '11218': 'Снежинск', '11158': 'Курганская область', '53': 'Курган',
           '11162': 'Свердловская область', '54': 'Екатеринбург', '11164': 'Каменск-Уральский', '11168': 'Нижний Тагил',
           '11170': 'Новоуральск', '11171': 'Первоуральск', '11176': 'Тюменская область', '55': 'Тюмень',
           '11175': 'Тобольск', '11193': 'Ханты-Мансийский автономный округ', '57': 'Ханты-Мансийск', '973': 'Сургут',
           '1091': 'Нижневартовск', '59': 'Сибирь', '11318': '  Омская область', '66': 'Омск',
           '11316': 'Новосибирская область', '65': 'Новосибирск', '11314': 'Бердск', '11353': 'Томская область',
           '67': 'Томск', '11232': 'Ямало-Ненецкий автономный округ', '58': 'Салехард', '11235': 'Алтайский край',
           '197': 'Барнаул', '975': 'Бийск', '11251': 'Рубцовск', '10231': 'Республика Алтай', '11319': 'Горно-Алтайск',
           '11282': 'Кемеровская область', '64': 'Кемерово', '11287': 'Междуреченск', '237': 'Новокузнецк',
           '11291': 'Прокопьевск', '11340': 'Республика Хакасия', '1095': 'Абакан', '10233': 'Республика Тыва',
           '11333': 'Кызыл', '11309': 'Красноярский край', '62': 'Красноярск', '11302': 'Ачинск', '11311': 'Норильск',
           '20086': 'Железногорск', '11266': 'Иркутская область', '63': 'Иркутск', '976': 'Братск',
           '11330': 'Республика Бурятия', '198': 'Улан-Удэ', '21949': 'Забайкальский край', '68': 'Чита',
           '73': 'Дальневосточный федеральный округ', '11443': 'Якутия', '74': 'Якутск', '11375': 'Амурская область',
           '77': 'Благовещенск', '10243': 'Еврейская автономная область', '11393': 'Биробиджан',
           '11409': 'Приморский край', '75': 'Владивосток', '974': 'Находка', '11426': 'Уссурийск',
           '10251': 'Чукотский автономный округ', '11458': 'Анадырь', '11398': 'Камчатский край',
           '78': 'Петропавловск-Камчатский', '11403': 'Магаданская область', '79': 'Магадан',
           '11450': 'Сахалинская область', '80': 'Южно-Сахалинск', '11457': 'Хабаровский край', '76': 'Хабаровск',
           '11453': 'Комсомольск-на-Амуре'}  # constants for statistic
REGIONS_KEYS = list(REGIONS.values())


def get_key(value):
    for k, v in REGIONS.items():
        if v == value:
            return k


def get_statistic(uid):
    print(uid)
    statistic = (requests.get('https://yastat.net/s3/milab/2020/covid19-stat/data/data-by-region/'
                              + str(uid) + '.json')).json()
    statistic = statistic['info']
    return statistic


def save_users(users):
    with open('users.txt', 'w') as outfile:
        json.dump(users, outfile)


def send_message():
    title = news.govno.ones(news.govno.news)
    for i in list(users.keys()):
        try:
            stat = get_statistic((users[str(i)])[0])
            bot.send_photo(i, image.image.gen_text(str(stat["cases"]), str(stat["deaths"]), str(stat["cured"]),
                                                   str(stat["cases_delta"]),
                                                   str(stat["deaths_delta"]), str(stat["cured_delta"])),
                           caption=f"Ежедневаная рассылка, что бы отписаться зайдите в настройки\n"
                                   f"А главная нововсть прошедшего дня:\n<a href='{title[1]}'>{title[0]}</a>",
                           parse_mode='HTML')
        except:
            pass


schedule.every().day.at("15:55").do(send_message)
title = news.govno.ones(news.govno.news)
print(title)


def schedule_task():
    while True:
        schedule.run_pending()
        time.sleep(1)


x = threading.Thread(target=schedule_task)
x.start()


def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––")
            print(f'{m.chat.first_name}[{m.chat.id}][{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}]: {m.text}')
            with open('logs.txt', 'a', encoding='utf-8') as logs_file:
                logs_file.write("––––––––––––––––––––––––––––––––––––––––––––––––––––––\n")
                logs_file.write(
                    f'{m.chat.first_name}[{m.chat.id}][{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}]: {m.text}\n')


bot.set_update_listener(listener)


def menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    settings = InlineKeyboardButton("Настройки", callback_data="settings")
    statistic = InlineKeyboardButton("Статистика", callback_data="statistic")
    statistic_by_location = InlineKeyboardButton("Статистика региона по вашей локации",
                                                 callback_data="statistic_by_location")
    news = InlineKeyboardButton("Сводка новостей", callback_data="news")
    markup.add(settings, statistic, statistic_by_location, news)
    return markup


def settings_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    subscription = InlineKeyboardButton("Подписка", callback_data="subscription")
    setup_location = InlineKeyboardButton("Ваша любимая локация", callback_data="setup_location")
    back = InlineKeyboardButton("В главное меню", callback_data="back")
    markup.add(subscription, setup_location, back)
    return markup


def back_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    back = InlineKeyboardButton("Назад", callback_data="back")
    markup.add(back)
    return markup


def choose_yes():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    subscribe = InlineKeyboardButton("Подписаться ✅", callback_data="subscribe")
    markup.add(subscribe)
    return markup


def choose_no():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    unsubscribe = InlineKeyboardButton("Отписаться ❌", callback_data="unsubscribe")
    markup.add(unsubscribe)
    return markup


def obrabotka_new_location(message):
    try:
        reg = difflib.get_close_matches(str(message.text), REGIONS_KEYS)
        print(reg)
        users[str(message.chat.id)][0] = get_key(reg[0])
        save_users(users)
        bot.send_message(message.chat.id, f'Вы сменили свою локацию на {reg[0]}',
                         reply_markup=menu())
    except Exception as e:
        bot.send_message(message.chat.id, "Вы ввели какую-то белебрду, попробуйте снова", reply_markup=menu())


def obrabotka_location(message):
    if message.content_type == 'location':
        bot.delete_message(message.chat.id, message.message_id)
        geolocator = Nominatim(user_agent="tg_bot")
        location = geolocator.reverse(f"{str(message.location.latitude)}, {str(message.location.longitude)}")
        city = str(location).split(', ')[5]
        try:
            code = (difflib.get_close_matches(str(city), REGIONS_KEYS))[0]
        except:
            code = 'None'
        if users[str(message.chat.id)][0] is None:
            users[str(message.chat.id)][0] = get_key(code)
            save_users(users)
        stat = get_statistic((users[str(message.chat.id)])[0])
        bot.send_message(message.chat.id, f'Статистика по региону: {stat["full_name"]}\n'
                                          f'Всего заражено: {stat["cases"]} новых случаев {stat["cases_delta"]}\n'
                                          f'Выздоровело: {stat["cured"]} новых случаев {stat["cured_delta"]}\n'
                                          f'Умерло: {stat["deaths"]} новых случаев {stat["deaths_delta"]}',
                         reply_markup=back_menu())
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        bot.send_message(message.chat.id, "Похоже вы отправили мне не то. Повторите попытку:", reply_markup=menu())


def obrabotka(message):
    try:
        reg = difflib.get_close_matches(str(message.text), REGIONS_KEYS)
        print(reg)
        users[str(message.chat.id)][0] = get_key(reg[0])
        save_users(users)
        stat = get_statistic(get_key(reg[0]))
        bot.send_message(message.chat.id, f'<b>Статистика по региону</b>:\n<i>{stat["full_name"]}</i>\n'
                              f'<b>Всего заражено</b>:\n<i>{stat["cases"]}</i> новых случаев <i>{stat["cases_delta"]}</i>\n'
                              f'<b>Выздоровело</b>:\n<i>{stat["cured"]}</i> новых случаев <i>{stat["cured_delta"]}</i>\n'
                              f'<b>Умерло</b>:\n<i>{stat["deaths"]}</i> новых случаев <i>{stat["deaths_delta"]}</i>'
                         ,
                         parse_mode='HTML', reply_markup=back_menu())
    except Exception as e:
        bot.send_message(message.chat.id, "Вы ввели какую-то белебрду, попробуйте снова", reply_markup=menu())


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе узнать актуальную информацию о коронавирусе в "
                                      "твоем районе.\nВыбери действие:",
                     reply_markup=menu())
    if str(message.chat.id) not in users:
        users[str(message.chat.id)] = [None, False]
        save_users(users)


@bot.message_handler(
    content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker', 'contact'])
def error(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    print(type(message.chat.id))
    bot.send_message(message.chat.id, 'Воспользуйтесь предложенными кнопками. '
                                      'Если кнопки исчезли, введите команду /start')


@bot.message_handler(content_types=['location'])
def skhgjlh(message):
    obrabotka_location(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "subscription":
            if users[str(call.message.chat.id)][1]:
                bot.edit_message_text("Состояние подписки: активна", call.message.chat.id,
                                      call.message.message_id, reply_markup=choose_no())
            else:
                bot.edit_message_text("Состояние подписки: не активна",
                                      call.message.chat.id,
                                      call.message.message_id, reply_markup=choose_yes())
        elif call.data == "subscribe":
            bot.edit_message_text("Вы подписаны! ✅",
                                  call.message.chat.id,
                                  call.message.message_id, reply_markup=menu())
            users[str(call.message.chat.id)][1] = True
            save_users(users)
        elif call.data == "unsubscribe":
            bot.edit_message_text("Вы отписались и теперь не будете получать новости каждый день.",
                                  call.message.chat.id,
                                  call.message.message_id, reply_markup=menu())
            users[str(call.message.chat.id)][1] = False
            save_users(users)

        elif call.data == "back":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=menu())

        elif call.data == "settings":
            bot.edit_message_text("Настройки:",
                                  call.message.chat.id,
                                  call.message.message_id, reply_markup=settings_menu())

        elif call.data == 'statistic_by_location':
            location = bot.edit_message_text(
                'Если хочешь узнать статистику по коронавирусу в своем регионе, просто отправь мне свою геолокацию. '
                'Если ты хочешь добавить какой-либо город как постоянный, воспользуйся кнопкой "Статистика" в главном '
                'меню.',
                call.message.chat.id, call.message.message_id, reply_markup=back_menu())
            bot.register_next_step_handler(location, obrabotka_location)

        elif call.data == 'statistic':
            if users[str(call.message.chat.id)][0] is None:
                text = bot.send_message(call.message.chat.id, "Ух ты! Похоже у Вас не настроена ваша постоянная "
                                                              "локация!\nДавайте настроим! Отправьте город в котором "
                                                              "вы живёте")
                bot.register_next_step_handler(text, obrabotka)
            else:
                stat = get_statistic((users[str(call.message.chat.id)])[0])
                bot.edit_message_text(f'<b>Статистика по региону</b>:\n<i>{stat["full_name"]}</i>\n'
                                      f'<b>Всего заражено</b>:\n<i>{stat["cases"]}</i> новых случаев <i>{stat["cases_delta"]}</i>\n'
                                      f'<b>Выздоровело</b>:\n<i>{stat["cured"]}</i> новых случаев <i>{stat["cured_delta"]}</i>\n'
                                      f'<b>Умерло</b>:\n<i>{stat["deaths"]}</i> новых случаев <i>{stat["deaths_delta"]}</i>',
                                      call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=back_menu())
        elif call.data == "setup_location":
            text = bot.send_message(call.message.chat.id, "Что бы сменить постоянную локацию просто напишите новую!")
            bot.register_next_step_handler(text, obrabotka_new_location)
        elif call.data == 'news':
            news_list = news.govno.mnogo(news.govno.news)
            news_str = ''
            for i in range(1, 6):
                news_str += f"{str(i)}. <a href='{news_list[i][1]}'>{news_list[i][0]}</a>\n\n"
            bot.edit_message_text(news_str, call.message.chat.id, call.message.message_id, parse_mode='HTML',
                                  reply_markup=back_menu())

        bot.answer_callback_query(call.id)



    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        bot.send_message(452207570, f'Произошло падение(((\nОшибка:\n{e}')
