'''
Модуль для обработки всех типов сообщений, callback-ов в боте
'''

import os
import datetime
import traceback

from telebot import TeleBot, types
from django.core.paginator import Paginator

import utils
from call_types import CallTypes

from config import APP_DIR
from backend.models import Hotel, BotUser, Booking
from backend.templates import Messages, Keys


# Функция для получения информации об отеле
def get_hotel_info(hotel: Hotel):
    return Messages.HOTEL.format(
        title=hotel.title,
        rating=hotel.rating,
        region=hotel.region,
    )


# Функция для получения байт-кода картинки отеля
def get_hotel_image(hotel: Hotel):
    hotel_image_path = os.path.join(APP_DIR, hotel.image.name)
    with open(hotel_image_path, 'rb') as file:
        data = file.read()

    return data


# Функция-обработчик кнопки "Отели"
def hotel_callback_query_handler(bot: TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    page = call_type.page
    hotels = Hotel.hotels.all()
    paginator = Paginator(hotels, 1)
    page = paginator.get_page(page)
    hotel = page.object_list[0]
    hotel_info = get_hotel_info(hotel)
    image = get_hotel_image(hotel)
    keyboard = utils.make_page_keyboard(page, CallTypes.Hotel)
    booking_button = utils.make_inline_button(
        text=Keys.BOOKING,
        CallType=CallTypes.HotelBooking,
        hotel_id=hotel.id,
    )
    keyboard.add(booking_button)
    if call.message.content_type == 'photo':
        bot.edit_message_media(
            media=types.InputMediaPhoto(
                media=image,
                caption=hotel_info,
                parse_mode='HTML',
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=keyboard,
        )
    else:
        bot.send_photo(
            chat_id=call.message.chat.id,
            caption=hotel_info,
            photo=image,
            reply_markup=keyboard,
        )


# Функция-обработчик кнопки "Бронировать"
def hotel_booking_callback_query_handler(bot: TeleBot, call):
    call_type = CallTypes.parse_data(call.data)
    hotel_id = call_type.hotel_id
    hotel = Hotel.hotels.get(id=hotel_id)
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    user.bot_state = BotUser.State.BOOKING_DATE
    user.save()
    Booking.bookings.create(hotel=hotel, user=user)
    bot.send_message(chat_id, Messages.BOOKING_DATE)


# Функция-обработчик в момент, когда задается дата бронирования
def booking_date_message_handler(bot: TeleBot, message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    try:
        day, month, year = map(int, message.text.split('/'))
        date = datetime.date(year, month, day)
        booking = user.bookings.first()
        booking.date = date
        booking.save()
    except Exception:
        traceback.print_exc()
        bot.send_message(chat_id, Messages.BOOKING_DATE_ERROR)
        return

    bot.send_message(chat_id, Messages.BOOKING_DAYS)
    user = BotUser.objects.get(chat_id=chat_id)
    user.bot_state = BotUser.State.BOOKING_DAYS
    user.save()


# Функция-обработчик в момент, когда задается количество дней бронирования
def booking_days_message_handler(bot: TeleBot, message):
    chat_id = message.chat.id
    try:
        days = int(message.text)
        if days <= 0:
            raise ValueError

        booking = Booking.bookings.first()
        booking.days = days
        booking.save()
    except Exception:
        bot.send_message(chat_id, Messages.BOOKING_DAYS_ERROR)
        return
    else:
        user = BotUser.objects.get(chat_id=chat_id)
        user.bot_state = BotUser.State.NOTHING
        user.save()
        bot.send_message(chat_id, Messages.BOOKED)


# Функция для получения информации о бронировании
def get_booking_info(booking: Booking):
    return Messages.BOOKING.format(
        hotel_title=booking.hotel.title,
        date=booking.date,
        days=booking.days,
        id=booking.id,
    )


# Функция-обработчик кнопки "Бронирования"
def booking_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    call_type = CallTypes.parse_data(call.data)
    page = call_type.page
    bookings = user.bookings.all()
    if not bookings:
        bot.send_message(chat_id, Messages.NOT_BOOKINGS)
        return

    paginator = Paginator(bookings, 1)
    page = paginator.get_page(page)
    booking = page.object_list[0]
    booking_info = get_booking_info(booking)
    keyboard = utils.make_page_keyboard(page, CallTypes.Hotel)
    bot.edit_message_text(
        text=booking_info,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard,
    )
