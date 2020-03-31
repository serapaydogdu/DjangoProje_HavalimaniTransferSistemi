from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting

def index(request):       #setting ayarlarını getirecek . artık sitede görünecekler title ı vs.
    setting = Setting.objects.get(pk=1)    #templates in index inde değişiklik yapıldı.
    context = {'setting': setting}
    return render(request, 'index.html', context)  #index.htmle gönderdik.