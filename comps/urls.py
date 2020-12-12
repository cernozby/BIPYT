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

]