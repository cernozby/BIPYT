from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'comps'

urlpatterns = [
    path('administrace/zavody', views.CompsView, name='compsView'),
    url('NewComp', views.NewComp, name='NewComp'),
    path('deleteComp/<int:ids>', views.deleteComp, name='deleteComp'),
    path('administrace/kategorie/<int:ids>', views.categoryView, name='categoryView'),
    path('newCategory/<int:ids>', views.NewCategory, name='newCategory'),
    path('deleteCategory/<int:compId>/<int:categoryId>', views.deleteCategory, name='deleteCategory'),
    path('administrace/moji-zavodnici/registrace/<int:racerId>', views.registrationView, name='registration'),
    path('changeRegistration/<int:categoryId>/<int:racerId>', views.changeRegistration, name='changeRegistration'),
    path('seznam-prihlasenych', views.listOfCompWithRegistrateList, name='listOfComps'),
    path('seznam-prihlasenych/<int:compId>', views.listOfRegistrate, name='listOfRegistrate'),
    path('zadani-vysledku/<int:compId>/<int:categoryId>', views.changeResults, name='changeResult_2'),
    path('zadani-vysledku/<int:compId>', views.changeResults, name='changeResult_1'),
    path('zadani-vysledku', views.changeResults, name='changeResult_0'),
    path('vysledky/<int:compId>/<int:categoryId>', views.getResults, name='getResults_2'),
    path('vysledky/<int:compId>', views.getResults, name='getResults_1'),
    path('vysledky', views.getResults, name='getResults_0'),
    path('startovni-listina/<int:categoryId>', views.getStartsList, name='startersPdf'),
    path('administrace-uzivatelu', views.usersView, name='users'),
    path('deleteUser/<email>', views.deleteUser, name='deleteUser'),

    path('vysledky-pdf/<int:categoryId>', views.getResultPdf, name='resultPdf'),
    path('saveChangeResults/<int:compId>/<int:categoryId>', views.saveChangeResults, name='saveChangeResults'),

]
