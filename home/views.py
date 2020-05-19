import json
from unicodedata import category

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from car.models import Car, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ


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

def car_search(request):
    if request.method == 'POST':   #form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']    #formdan bilgiyi al
            catid = form.cleaned_data['catid']

            #cars = Car.objects.filter(title__icontains=query)   #Select * from car where title like %query%
            #return HttpResponse(cars)        #contains li dersek içerir demek ama icontains dersek büyük küçük harf ayrımı yapmadan arama yapacak.

               #get form data

            if catid ==0:
                cars = Car.objects.filter(title__icontains=query)
            else:
                cars = Car.objects.filter(title__icontains=query,category_id=catid)

            context = {'cars': cars,
                       'category': category,
                       }
            return render(request, 'car_search.html', context)

    return HttpResponseRedirect('/')

def car_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    car = Car.objects.filter(title__icontains=q)
    results = []
    for rs in car:
        car_json = {}
        car_json = rs.title
        results.append(car_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı Adı veya Şifre Yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)   #formumuzu signup ile ilişkilendirdik.
        if form.is_valid():               #valid kontrolü yaptık. şifre vs. uymuyorsa kurallara buna takılıyor.
            form.save()                   #kurallar dolu mu boş mu şifreler aynı mı uyuyor mu vs. dorm.save ile tüm elemanları alıp eşleştirdik.
            #return HttpResponse("Üye kaydedildi.") #kontrol ettim.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            #Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/user/user.png"
            data.save()
            messages.success(request, "Hoş Geldiniz.. Sitemize başarılı bir şekilde üye oldunuz. İyi yolculuklar dileriz.")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {'category': category,
               'faq': faq,
               }
    return render(request, 'faq.html', context)
