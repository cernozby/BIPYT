import io
import math
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
from collections import OrderedDict


class Comps(models.Model):
    name = models.CharField(max_length=50, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    type = models.CharField(max_length=50, null=True)
    min_age = models.IntegerField(null=True)
    max_age = models.IntegerField(null=True)
    state = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=150, null=True)

    def getDictCompType(self):
        return {0: 'obtížnost', 1: 'boulder', 2: 'rychlost'}

    def getDictState(self):
        return {'prepare': 'příprava', 'precomp': 'registrace', 'running': 'probíhá', 'end': 'ukončen'}

    def newComp(self, rq):
        Comps.objects.create(name=rq.POST['name'],
                             start_date=rq.POST['start_date'],
                             end_date=rq.POST['end_date'],
                             type=rq.POST['type'],
                             min_age=rq.POST['min_age'],
                             max_age=rq.POST['max_age'],
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

    # view final
    final = models.CharField(max_length=4, default=0, null=False)

    # lead results
    lead_route_1 = models.CharField(max_length=10, default=None, null=True)
    lead_route_2 = models.CharField(max_length=10, default=None, null=True)
    lead_route_final = models.CharField(max_length=10, default=None, null=True)

    # boulderResult
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

    # speed result
    speed_1 = models.CharField(max_length=10, default=None, null=True)
    speed_2 = models.CharField(max_length=10, default=None, null=True)
    speed_3 = models.CharField(max_length=10, default=None, null=True)
    speed_4 = models.CharField(max_length=10, default=None, null=True)

    def getPlace(self, data):
        result = {}
        i = 1
        beforeItem = []
        beforeKey = []
        sum = 0
        for key, item in data:
            if i > 1:
                if item != beforeItem[-1]:
                    listKey = 0
                    for k in beforeKey:
                        result[k] = float(sum / len(beforeKey))
                        listKey = listKey + 1
                    beforeItem = []
                    beforeKey = []
                    sum = 0
                beforeKey.append(key)
                beforeItem.append(item)
                sum = sum + i
                i = i + 1
            else:
                beforeKey.append(key)
                beforeItem.append(item)
                sum = sum + i
                i = i + 1

            listKey = 0
            for k in beforeKey:
                result[k] = sum / len(beforeKey)
                listKey = listKey + 1
        return result

    def getPlace(self, data, ResultType="classic"):
        result = {}
        i = 1
        beforeItem = []
        beforeKey = []
        sum = 0
        for key, item in data:
            if i > 1:
                if item != beforeItem[-1]:
                    listKey = 0
                    for k in beforeKey:
                        if ResultType == 'classic':
                            result[k] = float(sum / len(beforeKey))
                        else:
                            if len(beforeKey) == 1:
                                result[k] = str(i - 1) + '.'
                            else:
                                result[k] = str(i - len(beforeKey)) + '. - ' + str(i - 1) + '.'

                        listKey = listKey + 1
                    beforeItem = []
                    beforeKey = []
                    sum = 0
                beforeKey.append(key)
                beforeItem.append(item)
                sum = sum + i
                i = i + 1
            else:
                beforeKey.append(key)
                beforeItem.append(item)
                sum = sum + i
                i = i + 1

            listKey = 0
            for k in beforeKey:
                if ResultType == 'classic':
                    result[k] = sum / len(beforeKey)
                else:
                    if len(beforeKey) == 1:
                        result[k] = str(i - 1) + '.'
                    else:
                        result[k] = str(i - len(beforeKey)) + '. - ' + str(i - 1) + '.'
                listKey = listKey + 1
        return result

    def getLeadResult(self, data):
        dataSort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return self.getPlace(dataSort)

    def getBestTime(self, times):
        result = {}
        for key in times:
            best = float(9999)
            for k in times[key]:
                if times[key][k] is not None and best > float(times[key][k]) > 0:
                    best = float(times[key][k])

            result[key] = best

        return result

    def getPointsBoulder(self, boulders):
        boulderCount = {}
        pointsPerBoulder = {}
        result = {}

        boulderCount['boulder_1_zone'] = 0
        boulderCount['boulder_2_zone'] = 0
        boulderCount['boulder_3_zone'] = 0
        boulderCount['boulder_4_zone'] = 0
        boulderCount['boulder_5_zone'] = 0
        boulderCount['boulder_6_zone'] = 0
        boulderCount['boulder_1_top'] = 0
        boulderCount['boulder_2_top'] = 0
        boulderCount['boulder_3_top'] = 0
        boulderCount['boulder_4_top'] = 0
        boulderCount['boulder_5_top'] = 0
        boulderCount['boulder_6_top'] = 0

        for key in boulders:
            for k in boulders[key]:
                if boulders[key][k] is not 0:
                    boulderCount[k] = boulderCount[k] + 1

        for key in boulderCount:
            if boulderCount[key] is not 0:
                pointsPerBoulder[key] = float(100 / boulderCount[key])
            else:
                pointsPerBoulder[key] = float(100)

        for key in boulders:
            result[key] = 0
            for k in boulders[key]:
                if int(boulders[key][k]) > 0:
                    result[key] = result[key] + boulderCount[k]

        print(result)
        return result


    def getResults(self, categoryId):
        registrations = Registration.objects.filter(category_id=categoryId)
        category = Category.objects.get(id=categoryId)
        result = {}

        if category.comp.type == '0':
            reg1 = {}
            reg2 = {}
            qSum = {}

            for r in registrations:
                if r.lead_route_1 == '0' or r.lead_route_1 is None:
                    reg1[r.racer.id] = -1
                else:
                    reg1[r.racer.id] = int(r.lead_route_1)

                if r.lead_route_2 == '0' or r.lead_route_2 is None:
                    reg2[r.racer.id] = -1
                else:
                    reg2[r.racer.id] = int(r.lead_route_2)

            reg1 = self.getLeadResult(reg1)
            reg2 = self.getLeadResult(reg2)

            for x in registrations:
                qSum[x.racer.id] = round(math.sqrt(reg2[x.racer_id] * reg1[x.racer_id]), 2)

            qSum = self.getPlace(sorted(qSum.items(), key=lambda w: w[1], reverse=False), 'Place')

            for r in registrations:
                result[r.racer_id] = {'lead_route_1': reg1[r.racer_id],
                                      'lead_route_2': reg2[r.racer_id],
                                      'Q': round(math.sqrt(reg2[r.racer_id] * reg1[r.racer_id]), 2),
                                      'qSum': qSum[r.racer_id]}

            return result
        if category.comp.type == '1':
            boulders = {}
            for r in registrations:
                boulders[r.racer_id] = {'boulder_1_zone': r.boulder_1_zone,
                                        'boulder_2_zone': r.boulder_2_zone,
                                        'boulder_3_zone': r.boulder_3_zone,
                                        'boulder_4_zone': r.boulder_4_zone,
                                        'boulder_5_zone': r.boulder_5_zone,
                                        'boulder_6_zone': r.boulder_6_zone,
                                        'boulder_1_top': r.boulder_1_top,
                                        'boulder_2_top': r.boulder_2_top,
                                        'boulder_3_top': r.boulder_3_top,
                                        'boulder_4_top': r.boulder_4_top,
                                        'boulder_5_top': r.boulder_5_top,
                                        'boulder_6_top': r.boulder_6_top}

            boulders = self.getPointsBoulder(boulders)
            place = self.getPlace(sorted(boulders.items(), key=lambda w: w[1], reverse=True), 'Place')


            for r in registrations:
                result[r.racer_id] = {'boulderPoints': boulders[r.racer_id],
                                      'place': place[r.racer_id]}
            return result

        if category.comp.type == '2':
            speedTimes = {}

            for r in registrations:
                speedTimes[r.racer_id] = {'speed_1': r.speed_1,
                                          'speed_2': r.speed_2,
                                          'speed_3': r.speed_3,
                                          'speed_4': r.speed_4}

            bestTime = self.getBestTime(speedTimes)

            place = self.getPlace(sorted(bestTime.items(), key=lambda w: w[1], reverse=False), 'Place')
            for r in registrations:
                result[r.racer_id] = {'bestTime': bestTime[r.racer_id],
                                      'place': place[r.racer_id]}

            return result

    def saveResultPair(self, value: str, key: str):
        registrationId = key.split('_')[-1]
        keyToValue = key.replace('__' + registrationId, '')
        Registration.objects.filter(id=registrationId).update(**{keyToValue: value})

    def changeResult(self, request):
        for key, value in request.POST.dict().items():
            if key == 'csrfmiddlewaretoken':
                continue
            self.saveResultPair(value, key)


def getStartersPdf(categoryId):
    context_dict = {
        'racers': polls_models.Racer.objects.all().filter(registration__category_id=categoryId),
        'comp': Category.objects.get(id=categoryId).comp,
        'category': Category.objects.get(id=categoryId),
        'printTime': strftime("%d. %m. %Y %H:%M:%S", gmtime())
    }

    template = get_template('pdf/startersPdf.html')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def getResultToPdf(categoryId):
    registration = Registration()
    comp = Category.objects.get(id=categoryId).comp
    context_dict = {
        'comp': comp,
        'category': Category.objects.get(id=categoryId),
        'printTime': strftime("%d. %m. %Y %H:%M:%S", gmtime()),
        'registrations': Registration.objects.filter(category_id=categoryId),
        'place': registration.getResults(categoryId)
    }

    if comp.type == '0':
        template = get_template('pdf/leadResultsPdf.html')
    elif comp.type == '1':
        template = get_template('pdf/boulderResult.html')
    else:
        template = get_template('pdf/speedResultPdf.html')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
