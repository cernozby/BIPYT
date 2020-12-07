from django.db import models


class Racer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    born = models.IntegerField()

    def newRacer(self, first_name, last_name, born):
        if first_name is None or last_name is None or born is None or not born.isnumeric():
            raise Exception('newRacer: Argument can\'t be null')
        else:
            Racer.objects.create(first_name=first_name, last_name=last_name, born=born)


    def __str__(self):
        return self.first_name + ' ' + self.last_name



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
