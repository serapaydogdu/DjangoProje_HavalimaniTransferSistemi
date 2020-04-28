from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from car.models import CommentForm, Comment


def index(request):
    return HttpResponse("Car Page")

@login_required(login_url='/login') #check login
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')  # GET LAST URL
    if request.method == 'POST': #FORM POST EDİLDİYSE
        form = CommentForm(request.POST)
        if form.is_valid():      #car modelsten comment formundan subject rate comment geldi mi kontrol ediyor.
            current_user=request.user  #Access User session information

            data = Comment()           #Model ile bağlantı kuruyor.
            data.user_id = current_user.id
            data.car_id = id
            data.subject =form.cleaned_data['subject']
            data.comment =form.cleaned_data['comment']
            data.rate =form.cleaned_data['rate']
            data.ip =request.META.get('REMOTE_ADDR')  #CLİENT COMPUTER İP ADRESS
            data.save()    #veritabanına kaydettikk.

            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür ederiz.")

            return HttpResponseRedirect(url)
            #return HttpResponse('Kaydedildi.')

    messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen kontrol ediniz.")
    return HttpResponseRedirect(url)



