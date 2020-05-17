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


#@login_required(login_url='/login')  # Check Login
#def reservetocart(request, id):
#    url = request.META.get('HTTP_REFERER')  # get last url
#    current_user = request.user  # access user session information
# **********************************************
#    checkcar = ReservationCart.objects.filter(car_id=id)  # araç seçildi mi sorgusu sepette var mı
#    if checkcar:
#        control = 1  # varsa
#    else:
#        control = 0  # yoksa

#    if request.method == 'POST':  # form post edildiyse  ÜRÜN DETAY SAYFASINDAN GELDİYSE
#        form = ReservationCartForm(request.POST)
#        if form.is_valid():
#            if control == 1:  # ürün varsa güncelle
#                try:
#                    data = ReservationCart.objects.get(car_id=id)  # modelle bağlantı kurduk.
#                    data.quantity += form.cleaned_data['quantity']
#                    data.date = form.cleaned_data['date']
#                    data.save()  # veritabanına kaydet
#                    messages.success(request, "Araç transfer için rezerve seçilmiştir.")
#                except:
#                    messages.warning(request,
#                                     'Aracın transfer için rezerve seçiminde hata oluştu! Lütfen kontrol ediniz.')
#                    return HttpResponseRedirect(url)
#            else:  # ürün yokda ekle
#                try:
#                    data = ReservationCart()  # modelle bağlantı kurduk.
#                    data.user_id = current_user.id
#                    data.car_id = id
#                    data.quantity = form.cleaned_data['quantity']
#                    data.date = form.cleaned_data['date']
#                    data.save()  # veritabanına kaydet
#                    messages.success(request, "Araç transfer için rezerve seçilmiştir.")
#                    return HttpResponseRedirect(url)
#                except:
#                    messages.warning(request,
#                                     'Aracın transfer için rezerve seçiminde hata oluştu! Lütfen kontrol ediniz.')
#                    return HttpResponseRedirect(url)
#        else:
#            messages.warning(request, 'Aracın transfer için rezerve seçiminde hata oluştu! Lütfen kontrol ediniz.')
#
#    else:  # ÜRÜN DİREK EKLE BUTONUNA BASILDIYSA
#        if control == 1:  # ürün varsa güncelle
#            data = ReservationCart.objects.get(car_id=id)  # modelle bağlantı kurduk.
#            data.quantity += 1
#            data.save()  # veritabanına kaydet
#            messages.success(request, "Araç transfer için rezerve seçilmiştir.")
#        else:  # ürün yokda ekle
#            data = ReservationCart()  # model ile bağlantı kurduk.
#            data.user_id = current_user.id
#            data.car_id = id
#            data.quantity = 1
#            data.save()  # veritabanına kaydet
#            messages.success(request, "Araç transfer için seçilmiştir.")
#            return HttpResponseRedirect(url)
#
#    return HttpResponseRedirect(url)


#@login_required(login_url='/login')  # Check Login
#def reservationcart(request):
#    current_user = request.user
#    reservationcart = ReservationCart.objects.filter(user_id=current_user.id)
#    total = 0
#    for rs in reservationcart:
#        total += rs.car.price * rs.quantity
#
#    context = {'reservationcart': reservationcart,
#               'category': category,
#               'total': total,
#               }
#    return render(request, 'reservationcart_cars.html', context)


#@login_required(login_url='/login')  # Check Login
#def deletefromcart(request, id):
#    ReservationCart.objects.filter(id=id).delete()
#    messages.success(request, "Araç rezervasyondan silinmiştir.")
#    return HttpResponseRedirect("/reservationcart")


#@login_required(login_url='/login')  # Check Login
#def reservationcarold(request):
#   category = Category.objects.all()
#    current_user = request.user
#    reservationcart = ReservationCart.objects.filter(user_id=current_user.id)
#    total = 0
#    for rs in reservationcart:
#        total += rs.car.price + rs.quantity
#
#   if request.method == 'POST':
#       form = ReservationForm(request.POST)
#        if form.is_valid():
#            # Kredi kartı bilgilerini bankaya gönder onaylanırsa devam et olacaktı sorgulasaydık.
#            data = Reservation()
#            data.last_name = form.cleaned_data['last_name']
#            data.phone = form.cleaned_data['phone']
#            data.address = form.cleaned_data['address']
#            data.city = form.cleaned_data['city']
#            data.country = form.cleaned_data['country']
#            data.date = form.cleaned_data['date']
#           data.take_off = form.cleaned_data['take_off']
#            data.arrive = form.cleaned_data['arrive']
#            data.user_id = current_user.id
#            data.total = total
#            data.ip = request.META.get('REMOTE_ADDR')
#           reservationcode = get_random_string(5).upper()
#            data.code = reservationcode
#           data.save()

#           reservationcart = ReservationCart.objects.filter(user_id=current_user.id)
#            for rs in reservationcart:
#                detail = ReservationCar()
#                detail.reservaton_id = data.id  # reservation id  ->en son üretilen üstteki datadan gelen idyi kullanıyoruz.
#                detail.car_id = rs.car_id
#                detail.user_id = current_user.id
#                detail.quantity = rs.quantity
#                detail.price = rs.car.price
#                detail.amount = rs.amount
#                detail.save()
#
#                car = Car.objects.get(id=rs.car_id)
#                car.amount -= rs.quantity
#                car.save()
#
  #          ReservationCart.objects.filter(user_id=current_user.id).delete()
 #           messages.success(request, "Your reservation has been completed. Thank you'")
 #           return render(request, 'Reservation_Completed.html',
  #                        {'reservationcode': reservationcode, 'category': category})
##
   #     else:
  #          messages.warning((request, form.errors))
 #           return HttpResponseRedirect("/reservation/reservationcar")
#
  #  form = ReservationForm()
 #   profile = UserProfile.objects.get(user_id=current_user.id)
#    context = {'reservationcart': reservationcart,
#               'category': category,
#              'total': total,
#               'form': form,
#               'profile': profile,
#               }
#    return render(request, 'Reservation_Form.html', context)
