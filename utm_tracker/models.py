from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.name

class Via(models.Model):
    source = models.ForeignKey(Source, on_delete=models.SET_DEFAULT, default='direct', unique=True)
    visits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.source.name
