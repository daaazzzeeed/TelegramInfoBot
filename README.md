# TelegramInfoBot
I present you my tiny information bot for Telegram

This is the remastered version of one of my previous programms written for educational purposes. I refactored it, made it better and it will be updating weekly now!

From now bot is able to show today's weather (Beta and only in Moscow, Russia) and show my University Timetable, study week number and week specificator (even - numerator, odd - denominator). 

Bot has messages written in russian. 

Currently i'm working on it.


Constants.py file contains dictionary for correct weather imaging. 

I request weather from [Open Weather Map API](https://openweathermap.org/api)
It responses with JSON array which is then being processed with get_weather() function from main.py

All eternal work with Telegram API is courtesy of [pyTelegramBotApi](https://github.com/eternnoir/pyTelegramBotAPI)

Bot is able to work with commands '/start', '/schedule', '/weather'
