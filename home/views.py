from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):       #setting ayarlarını getirecek . artık sitede görünecekler title ı vs.
    setting = Setting.objects.get(pk=1)    #templates in index inde değişiklik yapıldı.
    context = {'setting': setting, 'page': 'home'}
    return render(request, 'index.html', context)  #index.htmle gönderdik.

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'hakkimizda.html', context)

def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'references.html', context)

def contact(request):
    if request.method =='POST':                       #FORM POSTT EDİLMİŞ İSE
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()                   #Model ile bağlantı kuruldu.
            data.name = form.cleaned_data['name']     #formdan bilgiyi aldık.
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()                                #veritabanına kaydettikk.
            messages.success(request, "Mesajınız başarılı bir şekilde gönderilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form}
    return render(request, 'contact.html', context)