from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting

def index(request):       #setting ayarlarını getirecek . artık sitede görünecekler title ı vs.
    setting = Setting.objects.get(pk=1)    #templates in index inde değişiklik yapıldı.
    context = {'setting': setting, 'page':'home'}
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
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'contact.html', context)