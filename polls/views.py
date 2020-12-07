from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *


def newRacer(request):
    if request.method == "POST":
        try:
            racer = Racer()
            if request.POST['edit'] is '0':
                racer.newRacer(request.POST['first_name'], request.POST['last_name'], request.POST['born'])
                messages.add_message(request, messages.INFO, 'Závodník byl úspěšně přidán!', 'fmgShort alert-success')
                message = 'Závodník byl úspěšně přidán!'
            else:
                editRacer = Racer.objects.get(id=request.POST['edit'])
                editRacer.first_name = request.POST['first_name']
                editRacer.last_name = request.POST['last_name']
                editRacer.born = request.POST['born']
                editRacer.save()
                message = 'Závodník byl úspěšně upraven!'
            messages.add_message(request, messages.INFO, message, 'fmgShort alert-success')
        except:
            messages.add_message(request, messages.ERROR, 'Operace se nepovedla!', 'fmgShort alert-danger')

        return HttpResponseRedirect('/administrace/moji-zavodnici')


def deleteRacer(request, ids):
    try:
        Racer.objects.get(id=ids).delete()
        messages.add_message(request, messages.INFO, 'Závodník byl smazán!', 'fmgShort alert-success')
    except:
        messages.add_message(request, messages.ERROR, 'Operace se nepovedla!', 'fmgShort alert-danger')

    return HttpResponseRedirect('/administrace/moji-zavodnici')


def HomepageDefaultView(request):
    return render(request, 'public/homepage.html')


def LoginView(request):
    if request.method == "POST":
        email = request.POST['email']
        passwd = request.POST['passwd']
        user = authenticate(request, username=email, password=passwd)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, 'Uživatel byl úspěšně prihlasen!',
                                 'fmgShort alert-success')
            return render(request, 'public/registration.html')
        else:
            messages.add_message(request, messages.ERROR, 'Prihlaseni se nepovedlo!',
                                 'fmgShort alert-danger')

    return render(request, 'public/login.html', dict(vysledek='aaa'))


def CompetitorsView(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup', 'fmgShort alert-danger')
        return render(request, 'public/homepage.html')
    else:
        return render(request, 'private/racers.html', dict(racers=Racer.objects.all()))
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup', 'fmgShort alert-danger')


def RegistrationVIew(request):
    if request.method == "POST":
        email = request.POST['email']
        passwd = request.POST['passwd']
        try:
            User.objects.get(email=email)
            messages.add_message(request, messages.INFO, 'Email jiz je v db', 'fmgShort alert-error')
        except:
            User.objects.create_user(email, email, passwd)
            messages.add_message(request, messages.INFO, 'Uživatel byl úspěšně zaregistrován!',
                                 'fmgShort alert-success')
    return render(request, 'public/registration.html')


def AdministrationView(request):
    if request.user.is_authenticated:
        return render(request, 'private/administration.html', dict(racers=Racer.objects.all()))
    else:
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup',
                             'fmgShort alert-danger')
        return render(request, 'public/homepage.html')


def myLogout(request):
    logout(request)
