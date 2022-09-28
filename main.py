from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from const import *
from keyboards.buttons import *
from transacts import *
import sqlite3
from datetime import datetime


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

connection = sqlite3.connect('adreses.db')
cursor = connection.cursor()

global mid


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, f"<b>Здрасвтвуй, {message.from_user.username}!</b>\nЯ тестовый бот <b>AMLCrypto!</b>\n\nПросто добавь адрес, за которым мы хотим наблюдать\n<b>Powered by @xen0x.</b>", parse_mode='html', reply_markup=keyb)


@dp.message_handler(lambda message: message.text == '🗒Список Адресов🗒')
async def list_adress(message: types.Message):
    user_adreses = connection.execute(f"SELECT ALL adreses, ticket FROM users WHERE name = '{message.from_user.username}'").fetchall()
    messageu = ''
    username = message.from_user.username
    for a in user_adreses:
        messageu = messageu + ' ' + str(a) + '\n'
    sqtime = datetime.now()
    cursor.execute(
        f"""INSERT INTO sqllogs (username, event, time) VALUES ('{str(username)}', 'get adreses', '{str(sqtime)}')""")
    connection.commit()
    await message.reply(f'<b>Твои Адреса:</b>\n\n{messageu}', parse_mode='html')


@dp.message_handler(lambda message: message.text == '❌Удалить Адреса❌')
async def list_adress(message: types.Message):
    cursor.execute(f"DELETE FROM users WHERE name = '{message.from_user.username}'")
    connection.commit()
    username = message.from_user.username
    sqtime = datetime.now()
    cursor.execute(
        f"""INSERT INTO sqllogs (username, event, time) VALUES ('{str(username)}', 'deleted username adreses', '{str(sqtime)}')""")
    connection.commit()
    await message.reply(f'<b>Твои Адреса были удалены!</b>', parse_mode='html')


@dp.message_handler(lambda message: message.text == '❌Удалить Адрес❌')
async def list_adress(message: types.Message):
    await delAdres.deladres.set()
    await message.reply(f'<b>Отравь адрес, который надо удалить</b>', parse_mode='html')


@dp.message_handler(state=delAdres.deladres)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['deladres'] = message.text

    async with state.proxy() as data:
        adres = data['deladres']
        cursor.execute(f"DELETE FROM users WHERE adreses = '{adres}'")
        connection.commit()

        username = message.from_user.username
        sqtime = datetime.now()
        cursor.execute(
            f"""INSERT INTO sqllogs (username, event, time) VALUES ('{str(username)}', 'deleted adres {str(adres)}', '{str(sqtime)}')""")
        connection.commit()
        await message.reply('<b>Адрес был удален!</b>\n\n', parse_mode='html', reply_markup=keyb)

        await state.finish()


@dp.message_handler(lambda message: message.text == '✅Добавить Адрес✅')
async def add_adress(message: types.Message):
    await addAdres.adres.set()
    await message.reply('Отправляй адрес')


@dp.message_handler(content_types=['text'], state=addAdres.adres)
async def load_adress(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adres'] = message.text
    await addAdres.next()
    await message.reply('Теперь введи для него заметку')


@dp.message_handler(state=addAdres.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    async with state.proxy() as data:
        id = message.from_user.id
        name = message.from_user.username
        adres = data['adres']
        ticket = data['name']
        cursor.execute(f"""INSERT INTO users (id, name, adreses, ticket) VALUES ('{id}', '{name}', '{adres}', '{ticket}')""")
        connection.commit()
        username = message.from_user.username
        sqtime = datetime.now()
        cursor.execute(
            f"""INSERT INTO sqllogs (username, event, time) VALUES ('{str(username)}', 'add adres {str(adres)}', '{str(sqtime)}')""")
        connection.commit()
        await message.reply('<b>Данные обновлены!</b>\n\nСписок Адресов пополнен', parse_mode='html', reply_markup=keyb)

        await state.finish()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(infinity_wallet_updates())
    loop.create_task(infinity_transctions_updates())
    executor.start_polling(dp, skip_updates=None)
