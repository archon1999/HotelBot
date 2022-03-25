'''
В этой модуле хранятся готовые функции для работы бота
'''

from telebot import types

from django.core.paginator import Page

from call_types import CallTypes
from backend.templates import Smiles


# Функция для создания страницы клавиатуры
# Используется в пунктах Отели и Бронирования для навигации
def make_page_keyboard(page: Page, CallType, **kwargs):
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    if page.has_previous():
        prev_page_button = make_inline_button(
            text=f'{Smiles.PREV_PAGE}',
            CallType=CallType,
            page=page.previous_page_number(),
            **kwargs,
        )
        buttons.append(prev_page_button)

    page_number_button = make_inline_button(
        text=str(page.number),
        CallType=CallTypes.Nothing,
    )
    buttons.append(page_number_button)

    if page.has_next():
        next_page_button = make_inline_button(
            text=f'{Smiles.NEXT_PAGE}',
            CallType=CallType,
            page=page.next_page_number(),
            **kwargs,
        )
        buttons.append(next_page_button)

    keyboard.add(*buttons)
    return keyboard


# Функция-шаблон для создания встроенных кнопок
def make_inline_button(text, CallType, **kwargs):
    call_type = CallType(**kwargs)
    call_data = CallTypes.make_data(call_type)
    button = types.InlineKeyboardButton(
        text=text,
        callback_data=call_data,
    )
    return button
