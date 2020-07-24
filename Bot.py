import config
import BDController
import requests


from state_bot import TestStates
from aiogram.utils import executor
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())


inline_button_link_create_bot = InlineKeyboardButton('Как создать бот?', url='https://telegra.ph/Add-Bot-to-Admins-Controller-FAQ-03-22', callback_data='link_create')
inline_kb_link = InlineKeyboardMarkup().add(inline_button_link_create_bot)

def inline_menu_bot(id):
    result = BDController.select_token_client_all(id)
    inline_kb_select = InlineKeyboardMarkup(row_width=1)
    inline_button_menu_bot = InlineKeyboardButton('Подключить бот', callback_data='create_bot')
    inline_kb_select.add(inline_button_menu_bot)
    for value in result:
        inline_kb_select.add(InlineKeyboardButton('%s(@%s)' % (value[3], value[4]), callback_data='bot_%s' % value[2]))
    return inline_kb_select


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Я помогаю создавать отложенные посты в Telegram каналы, прикреплять фото, реакции, клавиатуру и комментарии. \n\n /newpost - добваить пост \n\n'
                                                 '/addchannel - добавить канал\n' 
                                                 '/mychannels - управление каналами\n\n\n'
                                                 '/settings - настройка бота')
    id_client = BDController.select_id_client(message.from_user.id)
    if not id_client:
        BDController.insert_bd(message.from_user.id)


@dp.message_handler(commands=['addchannel'])
async def add_channel_bot(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    result = BDController.select_token_client_all(message.from_user.id)
    if len(result) > 0:
        await message.reply(config.select_bot, reply_markup=inline_menu_bot(message.from_user.id), reply=False)
    else:
        await message.reply(config.add_bot_channel, reply_markup=inline_kb_link, reply=False)
        await state.set_state(TestStates.all()[0])


@dp.message_handler(commands=['mychannels'])
async def channel_bot(message: types.Message):
    pass


@dp.message_handler(commands=['settings'])
async def setting_bot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Тут будут настройки')


@dp.message_handler(state=TestStates.STATE_ADD_TOKEN[0])
async def add_token_bot(message: types.Message):
    if message.text[:1] == '/':
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()

    else:
        info_bot = requests.get('https://api.telegram.org/bot%s/getMe' % message.text)
        first_name = info_bot.json()['result']['first_name']
        user_name = info_bot.json()['result']['username']
        print(info_bot.text)
        try:
            bot1 = Bot(token=message.text)
            result = BDController.select_token_client(message.from_user.id, message.text)
            print(result)
            if result == None:
                BDController.insert_token_bot(message.from_user.id, message.text, first_name, user_name)
                await message.reply("Бот успешно добавлен!", reply=False)
            else:
                await message.reply("Этот бот уже подключен к @Lexnom_bot", reply=False)
        except:
            await message.reply("Нет такого бота", reply=False)
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'create_bot')
async def switch_add_token(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=config.add_bot_channel, reply_markup=inline_kb_link)
    state = dp.current_state()
    await state.set_state(TestStates.all()[0])


@dp.callback_query_handler(lambda c: c.data[:4] == 'bot_')
async def menu_add_channel(callback:types.CallbackQuery):

    result = BDController.select_user_name_bot(callback.data[4:])
    inline_btn_back_markup = InlineKeyboardMarkup(row_width=1)
    inline_btn_back_markup.add(InlineKeyboardButton('Изменить бота', callback_data='back_menu_select'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Добавление канала\n\n'
                                                                                                               'Чтобы добавить канал, вы должны выполнить два следующих шага:\n\n'
                                                                                                               '1. Добавьте @%s в администраторы вашего канала\n'
                                                                                                               '2. Перешлите мне любое сообщение из вашего канала (вы также можете отправить @username '
                                                                                                               'или Group ID).' % result[0], reply_markup=inline_btn_back_markup)

@dp.callback_query_handler(lambda c: c.data == 'back_menu_select')
async def back_select_bot(callback: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=inline_menu_bot(callback.from_user.id), text=config.select_bot)





if __name__ == '__main__':
    executor.start_polling(dp)