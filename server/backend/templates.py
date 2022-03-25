from backend.models import Template


class Messages():
    MESSAGE = Template.messages.get(id=1).gettext()
    START_COMMAND = Template.messages.get(id=4).gettext()
    MENU = Template.messages.get(id=6).gettext()
    HOTEL = Template.messages.get(id=9).gettext()
    BOOKING_DATE = Template.messages.get(id=13).gettext()
    BOOKING_DAYS = Template.messages.get(id=14).gettext()
    BOOKING_DATE_ERROR = Template.messages.get(id=15).gettext()
    BOOKING_DAYS_ERROR = Template.messages.get(id=16).gettext()
    BOOKED = Template.messages.get(id=17).gettext()
    BOOKING = Template.messages.get(id=18).gettext()
    NOT_BOOKINGS = Template.messages.get(id=19).gettext()


class Keys():
    KEY = Template.keys.get(id=2).gettext()
    MENU = Template.keys.get(id=5).gettext()
    HOTELS = Template.keys.get(id=7).gettext()
    BOOKINGS = Template.keys.get(id=8).gettext()
    BOOKING = Template.keys.get(id=12).gettext()


class Smiles():
    SMILES = Template.smiles.get(id=3).gettext()
    PREV_PAGE = Template.smiles.get(id=10).gettext()
    NEXT_PAGE = Template.smiles.get(id=11).gettext()
