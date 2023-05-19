import os

import requests
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
bot = Bot(bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(msg: Message):
    btn1 = KeyboardButton('Tashkent')
    btn2 = KeyboardButton('Samarkand')
    btn3 = KeyboardButton('Jizzakh')
    btn4 = KeyboardButton('Sirdaryo')
    kyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kyb.add(btn1, btn2)
    kyb.add(btn3, btn4)
    await msg.answer('Botimizga xush kelibsiz! Ob-xavo ni ko\'rish uchun shahar nomini kiriting!', reply_markup=kyb)

@dp.message_handler(commands=['help'])
async def help(msg: Message):
    await msg.reply('Bu bot shunchaki test uchun.')
rsp = None
@dp.message_handler(lambda message: message.text in ['Tashkent', 'Samarkand', 'Jizzakh', 'Sirdaryo'])
async def get_weather(msg: Message):
    city = msg.text
    print(city)
    url = "https://api.openweathermap.org/data/2.5/weather"
    global rsp
    app_id = os.getenv('APPID')
    rsp = requests.post(url, params={'q': city, 'appid': app_id, 'units': 'metric', 'lang': 'UZ'})
    if rsp.status_code == 200:
        rsp = rsp.json()
        humidity_btn = KeyboardButton('Humidity')
        pressure_btn = KeyboardButton('Pressure')
        max_temp_btn = KeyboardButton('Max temp')
        min_temp_btn = KeyboardButton('Min temp')
        status_btn = KeyboardButton('Status')
        keyboard_button = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_button.add(humidity_btn, pressure_btn)
        keyboard_button.add(max_temp_btn, min_temp_btn, status_btn)
        await msg.answer(str(round(rsp['main']['temp'])) + '°C', reply_markup=keyboard_button)
    else:
        await msg.answer('Qandaydir xatolik!')

@dp.message_handler(lambda message: message.text in ['Humidity', 'Pressure', 'Max temp', 'Min temp', 'Status'])
async def get_other_datas(msg: Message):
    data = None
    print(rsp)
    if msg.text == 'Humidity':
        data = rsp['main']['humidity']
    elif msg.text == 'Pressure':
        data = rsp['main']['pressure']
    elif msg.text == 'Max temp':
        data = rsp['main']['temp_max']
    elif msg.text == 'Min temp':
        data = rsp['main']['temp_min']
    else:
        data = rsp['weather'][0]['main']
    
    await msg.answer(str(data), reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
