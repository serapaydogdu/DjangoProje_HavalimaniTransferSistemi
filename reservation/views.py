from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.utils.crypto import get_random_string

from car.models import Category, Car
from home.models import UserProfile
from reservation.models import Reservation, ReservationForm, ReservationCar


#from reservation.models import ReservationCartForm, ReservationCart,

def index(request):
    return HttpResponse("Reservation App")  # döngümün tamamlanıp tamamlanmadığını bu şekilde kontrol edebilirim.


@login_required(login_url='/login')  # Check Login
def reservationcar(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # access user session information
    car = Car.objects.get(pk=id)
    carUrl = "/car/" + str(id) + "/" + car.slug
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            data = Reservation()
            data.first_name = current_user.first_name
            data.last_name = current_user.last_name
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.date = form.cleaned_data['date']
            data.quantity = form.cleaned_data['quantity']
            data.take_off = form.cleaned_data['take_off']
            data.arrive = form.cleaned_data['arrive']
            data.user_id = current_user.id
            data.price = form.cleaned_data['price']
            data.ip = request.META.get('REMOTE_ADDR')
            reservationcode = get_random_string(5).upper()
            data.code = reservationcode
            data.save()

            detail = ReservationCar()
            detail.reservation = data
            detail.car_id = id
            detail.user_id = current_user.id
            detail.quantity = car.amount
            detail.price = car.price
            detail.amount = car.amount
            detail.date = form.cleaned_data['date']
            detail.save()
            car = Car.objects.get(id=id)
            car.amount -= 1
            car.save()

            messages.success(request, "Your reservation has been completed. Thank you'")
            return HttpResponseRedirect("/reservation/reservationcompleted/"+str(data.id))
        else:
            messages.warning(request, "Error <br>" + str(form.errors))
            return HttpResponseRedirect(carUrl)
    else:
        messages.warning(request, "No Post")
        return HttpResponseRedirect(carUrl)


@login_required(login_url='/login')
def reservationform(request, id):
    category = Category.objects.all()
    car = Car.objects.get(pk=id)
    profile = UserProfile.objects.get(user_id=request.user.id)
    total = car.price
    quantity = 1
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if(form.data['quantity'] is not None):
            total=car.price * int(form.data['quantity'])
            quantity = int(form.data['quantity'])
    context = {'id': id,
               'category': category,
               'total': total,
               'quantity': quantity,
               'profile': profile,
               }
    return render(request, 'Reservation_Form.html', context)


def reservationcompleted(request, id):
    category = Category.objects.all()
    reservation = Reservation.objects.get(pk=id)
    context = {
        'category': category, 'reservation': reservation,
    }
    return render(request, 'Reservation_Completed.html', context)

