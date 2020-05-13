from django.urls import path

from . import views

urlpatterns = [
    #path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('reservationcar/<int:id>', views.reservationcar, name='reservationcar'),
    path('reservationform/<int:id>', views.reservationform, name='reservationform'),
    path('reservationcompleted/<int:id>', views.reservationcompleted, name='reservationcompleted'),
]