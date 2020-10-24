import requests
import json
import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import schedule
import time
import threading
from geopy.geocoders import Nominatim

users = {}
with open('users.txt') as json_file:
    users = json.load(json_file)
    print(users.keys())
    
REGIONS = {'европа': '111', 'СНГ': '166', 'Универсальное': '318', 'Азия': '183', 'Россия': '225', 'Северо-Западный '
                                                                                                  'федеральный '
                                                                                                  'округ': '17',
           'Калининградская область': '10857', 'Калининград': '22', 'Мурманская область': '10897', 'Мурманск': '23',
           'Республика Карелия': '10933', 'Петрозаводск': '18', 'Санкт-Петербург': '2', 'Псковская область': '10926',
           'Псков': '25', 'Великие Луки': '10928', 'Новгородская область': '10904', 'Великий Новгород': '24',
           'Центральный федеральный округ': '3', 'Тверская область': '10819', 'Тверь': '14', 'Смоленская область':
               '10795', 'Смоленск': '12', 'Брянская область': '10650', 'Брянск': '191', 'Калужская область': '10693',
           'Калуга': '6', 'Обнинск': '967', 'Курская область': '10705', 'Курск': '8', 'Орловская область': '10772',
           'Орёл': '10', 'Тульская область': '10832', 'Тула': '15',
           'Москва': '213', 'Долгопрудный': '214', 'Дубна': '215', 'Зеленоград': '216', 'Пущино': '217',
           'Белгородская область': '10645', 'Белгород': '4', 'Липецкая область': '10712', 'Липецк': '9', 'Ярославская '
                                                                                                         'область':
               '10841', 'Ярославль': '16', 'Владимирская область': '10658', 'Владимир': '192', 'Александров':
               '10656', 'Гусь-Хрустальный': '10661', 'Муром': '10668', 'Ивановская область': '10687', 'Иваново': '5',
           'Рязанская область': '10776', 'Рязань': '11', 'Тамбовская область': '10802', 'Тамбов': '13', 'Воронежская '
                                                                                                        'область':
               '10672', 'Воронеж': '193', 'Южный федеральный округ': '26', 'Ростовская область': '11029',
           'Ростов-на-Дону': '39', 'Шахты': '11053', 'Таганрог': '971', 'Новочеркасск': '238', 'Волгодонск': '11036',
           'Краснодарский край': '10995', 'Краснодар': '35', 'Анапа': '1107', 'Новороссийск': '970', 'Сочи': '239',
           'Туапсе': '1058', 'Геленджик': '10990', 'Армавир': '10987', 'Ейск': '10993', 'Республика Адыгея': '11004',
           'Майкоп': '1093', 'Карачаево-Черкесская республика': '11020', 'Черкесск': '1104', 'Кабардино-Балкарская '
                                                                                             'республика': '11013',
           'Нальчик': '30', 'Северная Осетия': '11021', 'Владикавказ':
               '33', 'Республика Ингушетия': '11012', 'Чеченская республика': '11024', 'Чечня': '1106',
           'Республика Дагестан': '11010', 'Махачкала': '28', 'Ставропольский край': '11069', 'Ставрополь': '36',
           'Каменск-Шахтинский': '11043', 'Пятигорск': '11067', 'Минеральные Воды': '11063', 'Ессентуки': '11057',
           'Кисловодск': '11062', 'Республика Калмыкия': '11015', 'Элиста': '1094', 'Астраханская область': '10946',
           'Астрахань': '37', 'Волгоградская область': '10950', 'Волгоград': '38', 'Приволжский федеральный округ':
               '40', 'Поволжье': '11146', 'Саратов': '194', 'Жигулевск': '11132', 'Балаково':
               '11143', 'Пензенская область': '11095', 'Пенза': '49', 'Республика Мордовия': '11117', 'Саранск':
               '42', 'Ульяновская область': '11153', 'Ульяновск': '195', 'Самарская область': '11131',
           'Самара': '51', 'Тольятти': '240', 'Сызрань': '11139', 'Чувашская республика': '11156', 'Чебоксары': '45',
           'Республика Марий Эл': '11077', 'Йошкар-Ола': '41', 'Нижегородская область': '11079', 'Нижний Новгород':
               '47', 'Саров': '11083', 'Кировская область': '11070', 'Киров': '46', 'Костромская область': '10699',
           'Кострома': '7', 'Вологодская область': '10853', 'Вологда': '21', 'Архангельская область': '10842',
           'Архангельск': '20', 'Северодвинск': '10849', 'Ненецкий автономный округ': '10176', 'Республика Коми':
               '10939', 'Сыктывкар': '19', 'Удмуртская республика': '11148', 'Ижевск': '44', 'Республика Татарстан':
               '11119', 'Казань': '43', 'Набережные Челны': '236', 'Нижнекамск': '11127', 'Пермский край': '11108',
           'Пермь': '50', 'Республика Башкортостан': '11111', 'Уфа': '172', 'Нефтекамск': '11114', 'Салават':
               '11115', 'Стерлитамак': '11116', 'Оренбургская область': '11084', 'Оренбург': '48', 'Дзержинск':
               '972', 'Уральский федеральный округ': '52', '(Урал)  Челябинская область': '11225', 'Челябинск': '56',
           'Магнитогорск': '235', 'Снежинск': '11218', 'Курганская область': '11158', 'Курган': '53', 'Свердловская '
                                                                                                      'область':
               '11162', 'Екатеринбург': '54', 'Каменск-Уральский': '11164', 'Нижний Тагил': '11168', 'Новоуральск':
               '11170', 'Первоуральск': '11171', 'Тюменская область': '11176', 'Тюмень': '55', 'Тобольск': '11175',
           'Ханты-Мансийский автономный округ': '11193', 'Ханты-Мансийск': '57', 'Сургут': '973', 'Нижневартовск':
               '1091', 'Сибирь': '59', '  Омская область': '11318', 'Омск': '66',
           'Новосибирская область': '11316', 'Новосибирск': '65', 'Бердск': '11314', 'Томская область': '11353',
           'Томск': '67', 'Ямало-Ненецкий автономный округ': '11232', 'Салехард': '58', 'Алтайский край': '11235',
           'Барнаул': '197', 'Бийск': '975', 'Рубцовск': '11251', 'Республика Алтай': '10231', 'Горно-Алтайск':
               '11319', 'Кемеровская область': '11282', 'Кемерово': '64', 'Междуреченск': '11287', 'Новокузнецк':
               '237', 'Прокопьевск': '11291', 'Республика Хакасия': '11340', 'Абакан': '1095', 'Республика Тыва':
               '10233', 'Кызыл': '11333', 'Красноярский край': '11309', 'Красноярск': '62', 'Ачинск': '11302',
           'Норильск': '11311', 'Железногорск': '20086', 'Иркутская область': '11266', 'Иркутск': '63',
           'Братск': '976', 'Республика Бурятия': '11330', 'Улан-Удэ': '198', 'Забайкальский край': '21949',
           'Чита': '68', 'Дальневосточный федеральный округ': '73', 'Якутия':
               '11443', 'Якутск': '74', 'Амурская область': '11375', 'Благовещенск': '77', 'Еврейская автономная '
                                                                                           'область': '10243',
           'Биробиджан': '11393', 'Приморский край': '11409', 'Владивосток': '75', 'Находка': '974', 'Уссурийск':
               '11426', 'Чукотский автономный округ': '10251', 'Анадырь': '11458', 'Камчатский край': '11398',
           'Петропавловск-Камчатский': '78', 'Магаданская область': '11403', 'Магадан': '79', 'Сахалинская область':
               '11450', 'Южно-Сахалинск': '80', 'Хабаровский край': '11457', 'Хабаровск': '76',
           'Комсомольск-на-Амуре': '11453'}

token = '1383445486:AAExUfb7qDLtP7DsaYAZiSd6p_3hfPU1Qgc'
bot = telebot.TeleBot(token)


def send_message():
    bot.send_message(633161635, "gaysex")
    # TODO сделлать рассылку всем пользователям


schedule.every().day.at("14:19").do(send_message)


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
    markup.add(settings, statistic, statistic_by_location)
    return markup


def settings_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    subscription = InlineKeyboardButton("Подписка", callback_data="subscription")
    setup_location = InlineKeyboardButton("Ваша любимая локация", callback_data="setup_location")
    markup.add(subscription, setup_location)
    return markup


def back_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    back = InlineKeyboardButton("Назад", callback_data="back1")
    markup.add(back)
    return markup


def obrabotka_location(message):
    if message.content_type == 'location':
        bot.delete_message(message.chat.id, message.message_id)
        geolocator = Nominatim(user_agent="tg_bot")
        location = geolocator.reverse(f"{str(message.location.latitude)}, {str(message.location.longitude)}")
        city = str(location).split(', ')[5]
        try:
            code = REGIONS[city]
        except:
            code = 'None'
        bot.send_message(message.chat.id, f'Ваш город: {city}\nКод города: {code}',  reply_markup=back_menu())
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        bot.send_message(message.chat.id, "Похоже вы отправили мне не то. Повторите попытку:", reply_markup=menu())

def obrabotka(message):
    users[str(message.chat.id)] = message.text
    with open('users.txt', 'w') as outfile:
        json.dump(users, outfile)
    if message.text == "Москва":
        bot.send_message(message.chat.id, "Moscow")



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "всем привет ето коронавирус бот тут мы будем слать вам спам и рофлан приколы",
                     reply_markup=menu())
    if str(message.chat.id) not in users:
        users[str(message.chat.id)] = [None, False]
        with open('users.txt', 'w') as outfile:
            json.dump(users, outfile)


@bot.message_handler(
    content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker', 'contact'])
def error(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    bot.send_message(message.chat.id, 'Воспользуйтесь предложенными кнопками. '
                                      'Если кнопки исчезли, введите команду /start')


@bot.message_handler(
    content_types=['location'])
def govno(message):
    print(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "back":
            bot.edit_message_text("Выбери предмет:", call.message.chat.id, call.message.message_id, reply_markup=menu())

        elif call.data == "back1":
            bot.edit_message_text("Всем привет ето коронавирус бот тут мы будем слать вам спам и рофлан приколы", call.message.chat.id, call.message.message_id, reply_markup=menu())

        elif call.data == 'logs':
            logs_txt = open('logs.txt', 'rb')
            bot.send_document(call.message.chat.id, logs_txt)
            logs_txt.close()

        elif call.data == 'statistic_by_location':
            location = bot.edit_message_text('Если хочешь узнать статистику по коронавирусу в своем регионе, просто отправь мне свою геолокацию. Если ты хочешь добавить какой-либо город как постоянный, воспользуйся кнопкой "Статистика" в главном меню.', call.message.chat.id, call.message.message_id,)
            bot.register_next_step_handler(location, obrabotka_location)

        elif call.data == 'statistic':
            if users[str(call.message.chat.id)][0] == None:
                bot.send_message(call.message.chat.id, "Ух ты! Похоже у вас не настроена ваша постоянная локация!")
                text = bot.send_message(call.message.chat.id, "Давайте настроим!\n Отправьте ваш постоянный регион")
                bot.register_next_step_handler(text, obrabotka)
            # TODO сделать отправление статистики

        bot.answer_callback_query(call.id)

    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        bot.send_message(452207570, f'Произошло падение(((\nОшибка:\n{e}')
