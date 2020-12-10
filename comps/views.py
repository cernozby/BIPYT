from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *


def NewComp(request):
    if request.method == "POST":
        message = ''
        try:
            comp = Comps()
            if request.POST['edit'] is '0':
                comp.newComp(request)
                message = 'Závod byl úspěšně přidán!'
            else:
                print(request.POST['edit'])
                comp.editComp(request)
                message = 'Závod byl úspěšně upraven!'
        except:
            message = 'Operace se nepovedla!'

        messages.add_message(request, messages.INFO, message, 'fmgShort alert-success')
        return HttpResponseRedirect('/administrace/zavody')


def CompsView(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup', 'fmgShort alert-danger')

    return render(request, 'private/comps.html', dict(comps=Comps.objects.all(),
                                                      result_system_dict=Comps().getDictResultSystem(),
                                                      comp_type_dict=Comps().getDictCompType(),
                                                      state_dict=Comps().getDictState()))


def deleteComp(request, ids):
    try:
        Comps.objects.get(id=ids).delete()
        messages.add_message(request, messages.INFO, 'Závod byl smazán!', 'fmgShort alert-success')
    except:
        messages.add_message(request, messages.ERROR, 'Operace se nepovedla!', 'fmgShort alert-danger')

    return HttpResponseRedirect('/administrace/zavody')
