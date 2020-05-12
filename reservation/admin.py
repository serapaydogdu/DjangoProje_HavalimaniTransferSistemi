from django.contrib import admin

# Register your models here.
from reservation.models import ReservationCart


class ReservationCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'date', 'price', 'quantity', 'amount']
    list_filter = ['user']

admin.site.register(ReservationCart, ReservationCartAdmin)
