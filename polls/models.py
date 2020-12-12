from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


class Racer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    born = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def newRacer(self, rq):
        print(User)
        if rq.POST['first_name'] is None or rq.POST['last_name'] is None or rq.POST['born'] is None or not rq.POST['born'].isnumeric():
            raise Exception('newRacer: Argument can\'t be null')

        else:
            Racer.objects.create(first_name=rq.POST['first_name'], last_name=rq.POST['last_name'], born=rq.POST['born'], user=rq.user)


    def __str__(self):
        return self.first_name + ' ' + self.last_name



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
