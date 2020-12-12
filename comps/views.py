from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *


# ----------------------Comps--------------------------------
def NewComp(request):
    if request.method == "POST":
        type = 'alert-success'
        try:
            comp = Comps()
            if request.POST['edit'] is '0':
                comp.newComp(request)
                message = 'Závod byl úspěšně přidán!'
            else:
                comp.editComp(request)
                message = 'Závod byl úspěšně upraven!'
        except:
            message = 'Operace se nepovedla!'
            type = 'alert-danger'

        messages.add_message(request, messages.INFO, message, 'fmgShort ' + type)
        return HttpResponseRedirect('/administrace/zavody')


def CompsView(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup', 'fmgShort alert-danger')
        return render(request, 'public/homepage.html')
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


# --------------------------category------------------------------

def categoryView(request, ids):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup', 'fmgShort alert-danger')
        return render(request, 'public/homepage.html')
    # dict(comp=Comps.objects.get(id=ids), categoryToComp=Category.objects.all().filter(comp_id=ids))
    return render(request, 'private/category.html',
                  dict(comp=Comps.objects.get(id=ids), categoryToComp=Category.objects.all().filter(comp_id=ids))
                  # categoryToComp = Category.objects.all().filter(comp_id=ids)
                  )


def NewCategory(request, ids):
    if request.method == "POST":
        type = 'alert-success'
        category = Category()
        try:
            if request.POST['edit'] is '0':
                category.newCategory(request)
                message = 'Kategorie byla úspěšně přidána!'
            else:
                category.editCategory(request)
                message = 'Kategorie byla úspěšně upravena!'
        except:
            message = 'Operace se nepovedla!'
            type = 'alert-danger'

        messages.add_message(request, messages.INFO, message, 'fmgShort ' + type)
    return HttpResponseRedirect('/administrace/kategorie/' + str(ids))


def deleteCategory(request, compId, categoryId):
    try:
        Category.objects.get(id=categoryId).delete()
        messages.add_message(request, messages.INFO, 'Kategorie byla smazána!', 'fmgShort alert-success')
    except:
        messages.add_message(request, messages.ERROR, 'Operace se nepovedla!', 'fmgShort alert-danger')

    return HttpResponseRedirect('/administrace/kategorie/' + str(compId))
