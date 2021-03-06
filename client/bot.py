'''
Основной модуль бота. Служит для запуска бота
'''

from telebot import TeleBot

import config
import commands
import handlers
from call_types import CallTypes

from backend.models import BotUser
from backend.templates import Keys


# Обработчики сообщении
message_handlers = {
    '/start': commands.start_command_handler,
    '/menu': commands.menu_message_handler,
    Keys.MENU: commands.menu_message_handler,
}

# Обработчики состоянии
state_handlers = {
    BotUser.State.BOOKING_DATE: handlers.booking_date_message_handler,
    BotUser.State.BOOKING_DAYS: handlers.booking_days_message_handler,
}

# Экземпляр бота
bot = TeleBot(
    token=config.TOKEN,
    num_threads=3,
    parse_mode='HTML',
)


# Функция для добавления в базу нового пользователя
def create_user(message) -> BotUser:
    return BotUser.objects.create(
        chat_id=message.chat.id,
        first_name=message.chat.first_name,
        last_name=message.chat.last_name,
        username=message.chat.username,
    )


# Обработчик всех типов сообщений
@bot.message_handler()
def message_handler(message):
    chat_id = message.chat.id
    if not BotUser.objects.filter(chat_id=chat_id).exists():
        create_user(message)

    user = BotUser.objects.get(chat_id=chat_id)
    if user.bot_state:
        state_handlers[user.bot_state](bot, message)
        return

    for text, handler in message_handlers.items():
        if message.text == text:
            handler(bot, message)
            break


# Обработчики callback-ов(встроенных кнопок)
callback_query_handlers = {
    CallTypes.Hotel: handlers.hotel_callback_query_handler,
    CallTypes.HotelBooking: handlers.hotel_booking_callback_query_handler,
    CallTypes.Booking: handlers.booking_callback_query_handler,
}


# Обработчик всех типов callback-ов(встроенных кнопок)
@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    call_type = CallTypes.parse_data(call.data)
    for CallType, handler in callback_query_handlers.items():
        if CallType == call_type.__class__:
            handler(bot, call)
            break


if __name__ == "__main__":
    # bot.polling()
    bot.infinity_polling()
