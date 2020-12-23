import io
from time import strftime, gmtime

from django.contrib.auth.models import User
from django.db import models
from django_enumfield import enum
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from polls import models as polls_models


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
        return {'prepare': 'příprava', 'precomp': 'registrace', 'running' : 'probíhá'}

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
        comp.state = rq.POST['state']
        comp.save()


class Category(models.Model):
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=50, default=None, null=True)
    year_from = models.IntegerField()
    year_to = models.IntegerField()
    comp = models.ForeignKey(Comps, on_delete=models.CASCADE, default=None, null=True)

    def newCategory(self, rq):
        comp = Comps.objects.get(id=rq.POST['comp_id'])
        if Category.objects.all().filter(comp=comp, name=rq.POST['name']).exists():
            raise Exception("Invalid name exeption. Name is already exist")
        Category.objects.create(name=rq.POST['name'], year_from=rq.POST['year_from'], year_to=rq.POST['year_to'],
                                comp=Comps.objects.get(id=rq.POST['comp_id']), sex=rq.POST['sex'])

    def editCategory(self, rq):
        category = Category.objects.get(id=rq.POST['edit'])
        category.sex = rq.POST['sex']
        category.year_to = rq.POST['year_to']
        category.year_from = rq.POST['year_from']
        category.name = rq.POST['name']

        category.save()

    def getYear(self):
        if self.year_from == self.year_to:
            return str(self.year_to)
        else:
            return str(self.year_from) + '-' + str(self.year_to)


class Registration(models.Model):
    racer = models.ForeignKey(polls_models.Racer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    #lead results
    lead_route_1 = models.CharField(max_length=10, default=None, null=True)
    lead_route_2 = models.CharField(max_length=10, default=None, null=True)
    lead_route_3 = models.CharField(max_length=10, default=None, null=True)
    lead_route_4 = models.CharField(max_length=10, default=None, null=True)
    lead_route_final = models.CharField(max_length=10, default=None, null=True)

    #boulderResult
    boulder_1_zone = models.CharField(max_length=10, default=None, null=True)
    boulder_1_top = models.CharField(max_length=10, default=None, null=True)
    boulder_2_zone = models.CharField(max_length=10, default=None, null=True)
    boulder_2_top = models.CharField(max_length=10, default=None, null=True)
    boulder_3_zone = models.CharField(max_length=10, default=None, null=True)
    boulder_3_top = models.CharField(max_length=10, default=None, null=True)
    boulder_4_zone = models.CharField(max_length=10, default=None, null=True)
    boulder_4_top = models.CharField(max_length=10, default=None, null=True)
    boulder_5_zone = models.CharField(max_length=10, default=None, null=True)
    boulder_5_top = models.CharField(max_length=10, default=None, null=True)
    boulder_6_zone = models.CharField(max_length=10, default=None, null=True)
    boulder_6_top = models.CharField(max_length=10, default=None, null=True)

    boulder_1_zone_final = models.CharField(max_length=10, default=None, null=True)
    boulder_1_top_final = models.CharField(max_length=10, default=None, null=True)
    boulder_2_zone_final = models.CharField(max_length=10, default=None, null=True)
    boulder_2_top_final = models.CharField(max_length=10, default=None, null=True)
    boulder_3_zone_final = models.CharField(max_length=10, default=None, null=True)
    boulder_3_top_final = models.CharField(max_length=10, default=None, null=True)
    boulder_4_zone_final = models.CharField(max_length=10, default=None, null=True)
    boulder_4_top_final = models.CharField(max_length=10, default=None, null=True)

    #speed result
    speeed_1 = models.CharField(max_length=10, default=None, null=True)
    speeed_2 = models.CharField(max_length=10, default=None, null=True)
    speeed_3 = models.CharField(max_length=10, default=None, null=True)
    speeed_4 = models.CharField(max_length=10, default=None, null=True)







def getStartersPdf(categoryId):
    context_dict = {
        'racers': polls_models.Racer.objects.all().filter(registration__category_id=categoryId),
        'comp': Category.objects.get(id=categoryId).comp,
        'printTime': strftime("%d. %m. %Y %H:%M:%S", gmtime())
    }

    template = get_template('pdf/startersPdf.html')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



