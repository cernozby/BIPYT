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
