from django.db import models
from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString


# Класс для описания пользователя в боте
class BotUser(models.Model):
    class State(models.IntegerChoices):
        NOTHING = 0
        BOOKING_DATE = 1
        BOOKING_DAYS = 2

    chat_id = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    bot_state = models.IntegerField(default=State.NOTHING,
                                    verbose_name='Состояние')

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name or ''])

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# Класс для описания отеля в боте
class Hotel(models.Model):
    hotels = models.Manager()
    title = models.CharField(max_length=255,
                             verbose_name='Название')
    image = models.ImageField(upload_to='backend/hotels',
                              verbose_name='Картинка')
    rating = models.FloatField(verbose_name='Рейтинг(из 10)')
    region = models.CharField(max_length=255,
                              verbose_name='Регион')

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

    def __str__(self):
        return self.title


# Класс для описания бронирование в боте
class Booking(models.Model):
    bookings = models.Manager()
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
        verbose_name='Отель',
        related_name='bookings',
    )
    user = models.ForeignKey(
        to=BotUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='bookings',
    )
    date = models.DateField(null=True)
    days = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


# Телеграм поддерживает некоторые теги
# Эта функция нужна для удаления неподдерживаемых тегов

def filter_tag(tag: Tag, ol_number=None):
    if isinstance(tag, NavigableString):
        text = tag
        text = text.replace('<', '&#60;')
        text = text.replace('>', '&#62;')
        return text

    html = str()
    li_number = 0
    for child_tag in tag:
        if tag.name == 'ol':
            if child_tag.name == 'li':
                li_number += 1
        else:
            li_number = None

        html += filter_tag(child_tag, li_number)

    # Поддерживаемые теги телеграмом
    format_tags = ['strong', 'em', 'pre', 'b', 'u', 'i', 'code']
    if tag.name in format_tags:
        return f'<{tag.name}>{html}</{tag.name}>'

    if tag.name == 'a':
        return f"""<a href="{tag.get("href")}">{tag.text}</a>"""

    if tag.name == 'li':
        if ol_number:
            return f'{ol_number}. {html}'
        return f'•  {html}'

    if tag.name == 'br':
        html += '\n'

    if tag.name == 'span':
        styles = tag.get_attribute_list('style')
        if 'text-decoration: underline;' in styles:
            return f'<u>{html}</u>'

    if tag.name == 'ol' or tag.name == 'ul':
        return '\n'.join(map(lambda row: f'   {row}', html.split('\n')))

    return html


def filter_html(html: str):
    soup = BeautifulSoup(html, 'lxml')
    return filter_tag(soup)


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Template.Type.MESSAGE)


class KeyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Template.Type.KEY)


class SmileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Template.Type.SMILE)


# Класс для описания шаблона, используемые в боте
# Шаблоны разделены на 3 категории
class Template(models.Model):
    class Type(models.IntegerChoices):
        MESSAGE = 1, 'Сообщение'
        KEY = 2, 'Кнопка'
        SMILE = 3, 'Смайлик'

    templates = models.Manager()
    messages = MessageManager()
    keys = KeyManager()
    smiles = SmileManager()

    type = models.IntegerField(choices=Type.choices)
    title = models.CharField(max_length=255)
    body = RichTextField()

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def gettext(self):
        return filter_html(self.body)

    def __str__(self):
        return self.body
