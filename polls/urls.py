from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'polls'


urlpatterns = [
    path('', views.HomepageDefaultView),
    url('myLogout', views.myLogout, name='myLogout'),
    path('prihlaseni', views.LoginView, name='login'),
    path('administrace', views.AdministrationView, name='administration'),
    path('administrace/moji-zavodnici', views.CompetitorsView),
    url('newRacer', views.newRacer, name='newRacer'),
    path('deleteRacer/<int:ids>', views.deleteRacer, name='deleteRacer'),
    path('regitrace', views.RegistrationVIew, name='registration'),
]