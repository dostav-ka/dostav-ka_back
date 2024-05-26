from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
