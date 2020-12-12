from django.db import models
from django_enumfield import enum

from semestralka import settings


class Comps(models.Model):
    name = models.CharField(max_length=50, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    type = models.CharField(max_length=50, null=True)
    min_age = models.IntegerField(null=True)
    max_age = models.IntegerField(null=True)
    result_system = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    is_final = models.IntegerField(null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=150, null=True)

    def getDictResultSystem(self):
        return {0: 'zavodní', 1: 'amatérské'}

    def getDictCompType(self):
        return {0: 'obtížnost', 1: 'boulder', 2: 'rychlost'}

    def getDictState(self):
        return {'prepare': 'příprava'}

    def newComp(self, rq):
        Comps.objects.create(name=rq.POST['name'],
                             start_date=rq.POST['start_date'],
                             end_date=rq.POST['end_date'],
                             type=rq.POST['type'],
                             min_age=rq.POST['min_age'],
                             max_age=rq.POST['max_age'],
                             result_system=rq.POST['result_system'],
                             is_final=rq.POST['is_final'],
                             city=rq.POST['city'],
                             address=rq.POST['address'],
                             state='prepare'
                             )

    def editComp(self, rq, state=None):
        comp = Comps.objects.get(id=rq.POST['edit'])
        comp.name = rq.POST['name']
        comp.start_date = rq.POST['start_date']
        comp.end_date = rq.POST['end_date']
        comp.type = rq.POST['type']
        comp.min_age = rq.POST['min_age']
        comp.max_age = rq.POST['max_age']
        comp.result_system = rq.POST['result_system']
        comp.is_final = rq.POST['is_final']
        comp.city = rq.POST['city']
        comp.address = rq.POST['address']
        if state:
            comp.state = 'prepare'
        comp.save()


class Category(models.Model):
    name = models.CharField(max_length=50)
    year_from = models.IntegerField()
    year_to = models.IntegerField()
    comp = models.ForeignKey(Comps, on_delete=models.CASCADE, default=None, null=True)

    def newCategory(self, rq):
        comp = Comps.objects.get(id=rq.POST['comp_id'])
        if Category.objects.all().filter(comp=comp, name=rq.POST['name']).exists():
            raise Exception("Invalid name exeption. Name is already exist")
        Category.objects.create(name=rq.POST['name'], year_from=rq.POST['year_from'], year_to=rq.POST['year_to'],
                                comp=Comps.objects.get(id=rq.POST['comp_id']))

    def editCategory(self, rq):
        category = Category.objects.get(id=rq.POST['edit'])
        category.year_to = rq.POST['year_to']
        category.year_from = rq.POST['year_from']
        category.name = rq.POST['name']

        category.save()

    def getYear(self):
        if self.year_from == self.year_to:
            return str(self.year_to)
        else:
            return str(self.year_from) + '-' + str(self.year_to)