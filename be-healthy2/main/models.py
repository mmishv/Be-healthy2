from django.db import models


class Calculator(models.Model):
    sex = models.CharField(max_length=10, default='female')
    age = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    activity = models.CharField(max_length=50, default=1)
    goal = models.CharField(max_length=50, default=1)
