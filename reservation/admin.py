from django.contrib import admin

# Register your models here.
from reservation.models import ReservationCar, Reservation


#from reservation.models import ReservationCart

#class ReservationCartAdmin(admin.ModelAdmin):
#    list_display = ['user', 'car', 'date', 'price', 'quantity', 'amount']
#    list_filter = ['user']

class ReservationCarline(admin.TabularInline):
    model = ReservationCar
    readonly_fields = ('user','car','price','quantity','amount','date')
    can_delete = False        #rezervasyon silinmemeli.
    extra = 0

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone','city', 'date', 'take_off', 'arrive',  'price','adminnote', 'status']
    list_filter = ['status']
    readonly_fields = ('user','first_name','last_name','address','city','country','date','phone','ip','price','date', 'take_off', 'arrive','quantity')
    can_delete = False
    inlines = [ReservationCarline]  #aynı sayfada göster rezerv. a ait ürünleri

class ReservationCarAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'date', 'price', 'quantity', 'amount']
    list_filter = ['user']

#admin.site.register(ReservationCart, ReservationCartAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationCar, ReservationCarAdmin)
