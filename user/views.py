from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from car.models import Category, Comment
from home.models import UserProfile
from reservation.models import Reservation, ReservationCar
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')  # Check Login
def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access User session information

    profile = UserProfile.objects.get(user_id=current_user.id)
    #return  HttpResponse(profile)
    context = {'category': category,
               'profile': profile,
               }
    return render(request, 'user_profile.html',context)

@login_required(login_url='/login')  # Check Login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) #request.user is user data.
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated! ')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)   #model user data
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)   #güncelleme durumlarında bu kısım formu getir diyoruz. #"userprofile" model -> OneToOneField relation with user
        context = {'category': category,
                   'user_form': user_form,
                   'profile_form': profile_form,
                   }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')  # Check Login
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)   #important
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category
        })

@login_required(login_url='/login')  #check login
def comments(request):
    #return HttpResponse("Yorumlarınız ")

    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'comments': comments,
               }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')  #check login
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete() # başkasının kullanıcı değilse silmemesi ve istenen yorumun id uyuşaması halinde silinmesi sağlandı.
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')  # Check Login
def reservations(request):
    category = Category.objects.all()
    current_user = request.user
    reservations = Reservation.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'reservations': reservations,
               }
    #return HttpResponse("Rezervasyon Listesi")
    return render(request, "user_reservations.html", context)

@login_required(login_url='/login')  # Check Login
def reservationdetail(request,id):
    category = Category.objects.all()
    current_user = request.user
    reservation = Reservation.objects.get(user_id=current_user.id, id=id)   #güvenlik açığını önlemek için..
    reservationitems = ReservationCar.objects.filter(reservation_id=id)
    context = {'category': category,
               'reservation': reservation,
               'reservationitems': reservationitems,
               }
    #return HttpResponse(str(id))
    return render(request, "user_reservation_detail.html", context)