from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from main.models import Salon


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='salon_masters')
    telephone = PhoneNumberField(null=True)

    class Meta:
        verbose_name = 'Master'
        verbose_name_plural = 'Masters'

    def __str__(self):
        return self.user.__str__()
    