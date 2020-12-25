import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from polls import models
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


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
    if not request.user.is_superuser:
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
    if not request.user.is_superuser:
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup', 'fmgShort alert-danger')
        return render(request, 'public/homepage.html')
    return render(request, 'private/category.html',
                  dict(comp=Comps.objects.get(id=ids), categoryToComp=Category.objects.all().filter(comp_id=ids))
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


# --------------------------registration------------------------------

def registrationView(request, racerId):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Neoprávnění přístup', 'fmgShort alert-danger')
        return render(request, 'public/homepage.html')
    return render(request, 'private/registration.html',
                  dict(comps=Comps.objects.all().filter(state='precomp'), comp_type_dict=Comps().getDictCompType(),
                       registration=Registration, racer=models.Racer.objects.get(id=racerId))
                  )


def changeRegistration(request, categoryId, racerId):
    message = 'Operace se nepovedla!'
    type = 'alert-success'
    category = Category.objects.get(id=categoryId)
    racer = models.Racer.objects.get(id=racerId)
    registration = Registration.objects.all().filter(category=category, racer=racer)
    try:
        if not registration:
            Registration.objects.create(category=category, racer=racer)
            message = 'Závodník byl úspěšně přihlášen.'
        else:
            registration.delete()
            message = 'Závodník byl úspěšně odhlášen.'
    except:
        type = 'alert-danger'

    messages.add_message(request, messages.INFO, message, 'fmgShort ' + type)
    return HttpResponseRedirect('/administrace/moji-zavodnici/registrace/' + str(racerId))


# --------------------------listOfCompWithpublicRegistarteList------------------------------

def listOfCompWithRegistrateList(request):
    categories = Category.objects.all().filter()
    comps = Comps.objects.all().filter(state__in=('precomp', 'running'))
    return render(request, 'public/listOfCompsWithRegistrate.html', dict(comps=comps))


def listOfRegistrate(request, compId):
    return render(request, 'public/listOfRegistrate.html', dict(categories=Category.objects.all().filter(comp_id=compId)))


# --------------------------listOfCompWithpublicRegistarteList------------------------------
def getStartsList(request, categoryId):
    pdf = getStartersPdf(categoryId)
    return HttpResponse(pdf, content_type='application/pdf')



def changeResults(request, compId=None, categoryId=None):
    dictToRender = dict(compId=compId, categoryId=categoryId)
    if compId and categoryId:
        dictToRender['category'] = Category.objects.get(id=categoryId)
        dictToRender['comp'] = Comps.objects.get(id=compId)
        dictToRender['registrations'] = Registration.objects.filter(category_id=categoryId, )
    elif compId:
        dictToRender['categories'] = Category.objects.filter(comp_id=compId)
        dictToRender['comp'] = Comps.objects.get(id=compId)
    else:
        dictToRender['comps'] = Comps.objects.filter(state='running')
    return render(request, 'private/changeResults.html', dictToRender)


def saveChangeResults(request, compId, categoryId):
    registration = Registration()
    registration.changeResult(request)
    return HttpResponseRedirect('/zadani-vysledku/' + str(compId) + '/' + str(categoryId))

def getResults(request, compId=None, categoryId=None):
    dictToRender = dict(compId=compId, categoryId=categoryId)
    if compId and categoryId:
        registration = Registration()

        dictToRender['category'] = Category.objects.get(id=categoryId)
        dictToRender['comp'] = Comps.objects.get(id=compId)
        dictToRender['registrations'] = Registration.objects.filter(category_id=categoryId, )
        dictToRender['results'] = 1
        dictToRender['place'] = registration.getResults(categoryId)


    elif compId:
        dictToRender['categories'] = Category.objects.filter(comp_id=compId)
        dictToRender['comp'] = Comps.objects.get(id=compId)
    else:
        comps = Comps.objects.filter(state='running')
        dictToRender['comps'] = Comps.objects.filter(state='running')
        if comps.count() == 1:
            for comp in comps:
                dictToRender['compId'] = comp.id
                dictToRender['categories'] = Category.objects.filter(comp_id=comp.id)
                dictToRender['comp'] = Comps.objects.get(id=comp.id)

    return render(request, 'public/results.html', dictToRender)
