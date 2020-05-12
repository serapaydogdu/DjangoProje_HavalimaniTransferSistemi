from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    # ex: /home/5/
    # path('<int:question_id>/', views.detail, name='detail'),

    path('', views.index, name='index'),
    path('reservetocart/<int:id>', views.reservetocart, name='reservetocart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart')



]