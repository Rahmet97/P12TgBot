from aiogram.contrib.fsm_storage.memory import MemoryStorage

from states.states import UserState
from dispetcher import dp

import os

import requests
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)

logging.basicConfig(level=logging.INFO)

from callbacks.callback_handler import confirm, cancel

@dp.message_handler(commands=['start'])
async def start(msg: Message):
    btn_contact = KeyboardButton("📞 Telefon raqamni qoldirish", request_contact=True)
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(btn_contact)
    await msg.answer(
        'Botimizga xush kelibsiz! Botdan foydalanish uchun telefon raqamingizni qoldiring!',
        reply_markup=btn
    )
    await UserState.phone.set()


@dp.message_handler(state=UserState.phone, content_types=['text', 'contact'])
async def set_phone(msg: Message, state: FSMContext):
    if msg.contact:
        phone = msg.contact.phone_number
    else:
        phone = msg.text
    await state.update_data({
        'phone': phone
    })
    await msg.answer("Ism familiyangizni to'liq kiriting.", reply_markup=ReplyKeyboardRemove())
    await UserState.full_name.set()


@dp.message_handler(state=UserState.full_name)
async def set_fullname(msg: Message, state: FSMContext):
    full_name = msg.text
    await state.update_data({
        'full_name': full_name
    })
    await msg.answer("Necha yoshdasiz?")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_age(msg: Message, state: FSMContext):
    age = msg.text
    await state.update_data({
        'age': age
    })
    data = await state.get_data()
    fullname = data['full_name']
    phone = data['phone']
    age = data['age']
    data_msg = f'''
        Fullname: {fullname}
        phone: {phone}
        age: {age}
    '''
    confirm_btn = InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm")
    cancel_btn = InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")
    inline = InlineKeyboardMarkup()
    inline.add(confirm_btn, cancel_btn)
    await msg.answer(f"Siz muvaffaqiyatli ro'yhatdan o'tdingiz.\n{data_msg}", reply_markup=inline)


@dp.message_handler(commands=['help'])
async def help(msg: Message):
    await msg.reply('Bu bot shunchaki test uchun.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, allowed_updates=['message', 'callback_query'])
