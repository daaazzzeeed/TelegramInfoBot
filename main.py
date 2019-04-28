import telebot
import constants
import datetime
from telebot import types
import requests
import json
import math

bot = telebot.TeleBot(constants.token)
print('Started OK')


def init_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    weather_btn = types.KeyboardButton('/weather')
    schedule_button = types.KeyboardButton('/schedule')
    markup.add(weather_btn, schedule_button)
    return markup


def is_even(num):
    if num % 2 == 0:
        return 'Числитель'
    else:
        return 'Знаменатель'


def get_weather():
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Moscow,'
                                'ru&units=metric&APPID=2f63cb4d02e27e9b67128d8982fd7d43')
        data = response.json()
        weather = data['weather'][0]
        weather_id = weather['id']
        parameters = data['main']
        temp = parameters['temp']
        temp_min = parameters['temp_min']
        temp_max = parameters['temp_max']
        return [weather_id, temp, temp_min, temp_max]
    except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, TypeError,
            json.JSONDecodeError, TypeError) as error:
        print('Error occurred')
        return error


@bot.message_handler(commands=['start'])
def start(message):
        constants.requests_quantity += 1
        markup = init_markup()
        bot.send_message(message.chat.id, 'Привет, {name}! '.format(name=str(message.from_user.username)),
                         reply_markup=markup)
        print(message.from_user.username + ' использует бот')
        print('Количество обращений к боту: ', constants.requests_quantity)


@bot.message_handler(commands=['schedule'])
def send_schedule(msg):
    constants.requests_quantity += 1
    week_of_the_year = datetime.datetime.utcnow().isocalendar()[1]
    if week_of_the_year > 5:
        if week_of_the_year < 17+1+5:
            study_week = week_of_the_year - 5
            description = is_even(study_week)
            bot.send_message(msg.chat.id, '{week} неделя, {option}'.format(week=study_week, option=description))
        elif week_of_the_year > 30:
            study_week = week_of_the_year - 5 - 17 - 7
            description = is_even(study_week)
            bot.send_message(msg.chat.id, '{week} неделя, {option}'.format(week=study_week, option=description))
    bot.send_photo(msg.chat.id, photo=constants.photo_url)
    print('Количество обращений к боту: ', constants.requests_quantity)


@bot.message_handler(commands=['start'])
def start(message):
    constants.requests_quantity += 1
    bot.send_message(message.chat.id, 'Привет, {name}! '.format(name=str(message.from_user.username)),
                     reply_markup=init_markup())
    print('Количество обращений к боту: ', constants.requests_quantity)


@bot.message_handler(commands=['weather'])
def show_weather(message):
    constants.requests_quantity += 1
    try:
        print('Пользователь ' + str(message.from_user.username) + ' запросил погоду')
        weather = get_weather()
        bot.send_message(message.chat.id, 'Сейчас в городе Москва {temp}°, {description}'
                         .format(temp=math.ceil(weather[1]), description=constants.dictWeather.get(weather[0])))
        bot.send_message(message.chat.id, 'Сегодня будет от {temp_min}° до {temp_max}°'
                         .format(temp_min=math.ceil(weather[2]), temp_max=math.ceil(weather[3])))
        print('Количество обращений к боту: ', constants.requests_quantity)
    except TypeError as e:
        print('TypeError occured')
        print(e.args)
        bot.send_message(message.chat.id, 'Что-то пошло не так! Попробуй запросить погоду позже...')

try:
    bot.polling(none_stop=1)
except:
    print('Error occurred')