from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.forms import ModelForm

from car.models import Car


class Reservation(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    CHOICE = (
        ('Havalimani', 'Havalimani'),
        ('Havalimani-*', 'Havalimani-*'),
        ('Sehir-A', 'Sehir-A'),
        ('Sehir-B', 'Sehir-B'),
        ('Sehir-C', 'Sehir-C'),
        ('-', '-'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    quantity = models.IntegerField()
    date = models.DateTimeField(blank=True)
    time = models.TimeField(blank=True)
    take_off = models.CharField(blank=True, max_length=20, choices=CHOICE, default='-')
    arrive = models.CharField(blank=True, max_length=20, choices=CHOICE, default='-')
    price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'phone', 'quantity','address','city', 'date', 'time', 'take_off', 'arrive', 'country','price']


class ReservationCar(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.FloatField()
    date = models.DateTimeField(blank=True)
    price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.car.title
