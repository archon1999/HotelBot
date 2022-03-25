from django.contrib import admin

from .models import BotUser, Template, Hotel, Booking


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'get_full_name', 'username']
    search_fields = ['first_name', 'last_name', 'username']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'rating']
    search_fields = ['title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'hotel', 'user', 'date', 'days']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'title']
