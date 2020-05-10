from django.shortcuts import render

# Create your views here.
from car.models import Category
from home.models import UserProfile


def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access User session information

    profile = UserProfile.objects.get(user_id=current_user.id)
    #return  HttpResponse(profile)
    context = {'category': category,
               'profile': profile,
               }
    return render(request, 'user_profile.html',context)
