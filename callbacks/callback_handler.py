from aiogram.dispatcher import FSMContext

from states.states import UserState
from dispetcher import dp
from database.handler import add_user
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton


@dp.callback_query_handler(text="confirm", state=UserState.age)
async def confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    fullname = data['full_name']
    phone = data['phone']
    age = data['age']
    await state.finish()
    await state.reset_data()
    await add_user(full_name=fullname, phone=phone, age=int(age))
    await callback.message.answer("Ma'lumotlar saqlandi.")


@dp.callback_query_handler(text="cancel", state=UserState.age)
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await state.reset_data()
    await callback.message.delete()
    btn_contact = KeyboardButton("📞 Telefon raqamni qoldirish", request_contact=True)
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(btn_contact)
    await callback.message.answer(
        'Botimizga xush kelibsiz! Botdan foydalanish uchun telefon raqamingizni qoldiring!',
        reply_markup=btn
    )
    await UserState.phone.set()