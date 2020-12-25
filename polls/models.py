from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


class Racer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=50, default=None, null=True)
    club = models.CharField(max_length=50, default=None, null=True)
    born = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def newRacer(self, rq):
        if rq.POST['first_name'] is None or rq.POST['last_name'] is None or rq.POST['born'] is None or not rq.POST['born'].isnumeric():
            raise Exception('newRacer: Argument can\'t be null')

        else:
            Racer.objects.create(first_name=rq.POST['first_name'], last_name=rq.POST['last_name'], born=rq.POST['born'],club=rq.POST['club'], user=rq.user, sex=rq.POST['sex'])


    def __str__(self):
        return self.first_name + ' ' + self.last_name


