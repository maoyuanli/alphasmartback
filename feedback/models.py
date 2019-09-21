from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    comment = models.CharField(max_length=8000)
