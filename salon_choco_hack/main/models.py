from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Service(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Salon(models.Model):
    name = models.CharField( max_length=250)
    telephone = PhoneNumberField

    def __str__(self):
        return self.name

    