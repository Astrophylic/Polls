import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin  

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(boolean=True, ordering="pub_date", description="Published recently?")
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
class TimeRecord(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    fecha = models.DateField()
    duracion = models.FloatField()

    
    @property
    def duration(self):
        if self.duracion == 0 and self.fecha_checkout is not None:
            #restamos la fecha del checkout y la del checkin para saber la duracion
            self.duracion = int((self.fecha_checkout - self.fecha_checkin).total_seconds())
            self.save()
        elif self.fecha_checkout is None:
            #restamos el tiempo actual con la del checkin para saber cual es el checkout
            return int((timezone.now() - self.fecha_checkin).total_seconds())
        return self.duracion
    