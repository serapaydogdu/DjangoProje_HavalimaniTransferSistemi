from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import Category
from reservation.models import ReservationCartForm, ReservationCart


def index(request):
    return HttpResponse("Reservation App")  # döngümün tamamlanıp tamamlanmadığını bu şekilde kontrol edebilirim.


@login_required(login_url='/login')  # Check Login
def reservetocart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # access user session information
    # **********************************************
    checkcar = ReservationCart.objects.filter(car_id=id)  # araç seçildi mi sorgusu sepette var mı
    if checkcar:
        control = 1  # varsa
    else:
        control = 0  # yoksa

    if request.method == 'POST':  # form post edildiyse  ÜRÜN DETAY SAYFASINDAN GELDİYSE
        form = ReservationCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # ürün varsa güncelle
                try:
                    data = ReservationCart.objects.get(car_id=id)  # modelle bağlantı kurduk.
                    data.quantity += form.cleaned_data['quantity']
                    data.date = form.cleaned_data['date']
                    data.save()  # veritabanına kaydet
                    messages.success(request, "Araç transfer için rezerve seçilmiştir.")
                except:
                    messages.warning(request,
                                     'Aracın transfer için rezerve seçiminde hata oluştu! Lütfen kontrol ediniz.')
                    return HttpResponseRedirect(url)
            else:  # ürün yokda ekle
                try:
                    data = ReservationCart()  # modelle bağlantı kurduk.
                    data.user_id = current_user.id
                    data.car_id = id
                    data.quantity = form.cleaned_data['quantity']
                    data.date = form.cleaned_data['date']
                    data.save()  # veritabanına kaydet
                    messages.success(request, "Araç transfer için rezerve seçilmiştir.")
                    return HttpResponseRedirect(url)
                except:
                    messages.warning(request, 'Aracın transfer için rezerve seçiminde hata oluştu! Lütfen kontrol ediniz.')
                    return HttpResponseRedirect(url)
        else:
            messages.warning(request, 'Aracın transfer için rezerve seçiminde hata oluştu! Lütfen kontrol ediniz.')

    else:  # ÜRÜN DİREK EKLE BUTONUNA BASILDIYSA
        if control == 1:  # ürün varsa güncelle
            data = ReservationCart.objects.get(car_id=id)  # modelle bağlantı kurduk.
            data.quantity += 1
            data.save()  # veritabanına kaydet
            messages.success(request, "Araç transfer için rezerve seçilmiştir.")
        else:  # ürün yokda ekle
            data = ReservationCart()  # model ile bağlantı kurduk.
            data.user_id = current_user.id
            data.car_id = id
            data.quantity = 1
            data.save()  # veritabanına kaydet
            messages.success(request, "Araç transfer için seçilmiştir.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


@login_required(login_url='/login')  # Check Login
def reservationcart(request):
    category = Category.objects.all()
    current_user = request.user
    reservationcart = ReservationCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in reservationcart:
        total += rs.car.price * rs.quantity

    context = {'reservationcart': reservationcart,
               'category': category,
               'total': total,
               }
    return render(request, 'reservationcart_cars.html', context)


@login_required(login_url='/login')  # Check Login
def deletefromcart(request, id):
    ReservationCart.objects.filter(id=id).delete()
    messages.success(request, "Araç rezervasyondan silinmiştir.")
    return HttpResponseRedirect("/reservationcart")
