'''
Модуль предназначен для обработки команд в боте
'''

from telebot import TeleBot, types

from backend.templates import Messages, Keys

import utils
from call_types import CallTypes


# Функция обработки команды /start
def start_command_handler(bot: TeleBot, message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(Keys.MENU)
    bot.send_message(chat_id, Messages.START_COMMAND,
                     reply_markup=keyboard)

    hotels_button = utils.make_inline_button(
        text=Keys.HOTELS,
        CallType=CallTypes.Hotel,
        page=1,
    )
    bookings_button = utils.make_inline_button(
        text=Keys.BOOKINGS,
        CallType=CallTypes.Booking,
        page=1,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(hotels_button)
    keyboard.add(bookings_button)
    bot.send_message(chat_id, Messages.MENU,
                     reply_markup=keyboard)


# Функция обработки команды /menu
def menu_message_handler(bot: TeleBot, message):
    chat_id = message.chat.id
    hotels_button = utils.make_inline_button(
        text=Keys.HOTELS,
        CallType=CallTypes.Hotel,
        page=1,
    )
    bookings_button = utils.make_inline_button(
        text=Keys.BOOKINGS,
        CallType=CallTypes.Booking,
        page=1,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(hotels_button)
    keyboard.add(bookings_button)
    bot.send_message(chat_id, Messages.MENU,
                     reply_markup=keyboard)
