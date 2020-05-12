from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.forms import ModelForm

from car.models import Car


class ReservationCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.car.title

    @property
    def amount(self):
        return (self.quantity * self.car.price)

    @property
    def price(self):
        return (self.car.price)

class ReservationCartForm(ModelForm):
    class Meta:
        model = ReservationCart
        fields = ['quantity','date']  #bildirimde forma ihtiyacı var kaç adet olacağı
