from unicodedata import category

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import Car, Category, Images, Comment
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):       #setting ayarlarını getirecek . artık sitede görünecekler title ı vs.
    setting = Setting.objects.get(pk=1)    #templates in index inde değişiklik yapıldı.
    sliderdata = Car.objects.all()[:4]
    category = Category.objects.all()
    daycars = Car.objects.all()[:4]
    lastcars = Car.objects.all().order_by('-id')[:4]
    randomcars = Car.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata':sliderdata,
               'daycars': daycars,
               'lastcars': lastcars,
               'randomcars': randomcars,
               'car': Car
               }
    return render(request, 'index.html', context)  #index.htmle gönderdik.

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               'page': hakkimizda,
               }
    return render(request, 'hakkimizda.html', context)

def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               'page': references,
               }
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
    context = {'setting': setting,
               'form': form,
               'category': category,
               'page': contact,
               }
    return render(request, 'contact.html', context)

def category_cars(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    cars = Car.objects.filter(category_id=id, status='True')
    context = {'cars':cars,
               'category': category,
               'categorydata':categorydata
               }
    return render(request,'cars.html',context)

def car_detail(request,id,slug):
    #mesaj="Araç ",id,"/",slug
    category = Category.objects.all()
    car = Car.objects.get(pk=id)
    images = Images.objects.filter(car_id=id)
    comments = Comment.objects.filter(car_id=id, status='True')
    context = {'car': car,
               'category': category,
               'images': images,
               'comments': comments,
               }
    return render(request,'car_detail.html',context)
