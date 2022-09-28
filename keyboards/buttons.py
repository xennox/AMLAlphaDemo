from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

b1 = ('✅Добавить Адрес✅')
b2 = ('❌Удалить Адреса❌')
b3 = ('🗒Список Адресов🗒')
b4 = ('❌Удалить Адрес❌')


keyb = ReplyKeyboardMarkup(resize_keyboard=True)
keyb.add(b1).insert(b2).insert(b4).add(b3)


class addAdres(StatesGroup):
    adres = State()
    name = State()


class delAdres(StatesGroup):
    deladres = State()