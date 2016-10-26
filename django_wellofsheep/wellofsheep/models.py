from __future__ import unicode_literals

from django.db import models

# Create your models here.
class sheeps_table(models.Model):
    account = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    ip = models.CharField(max_length = 20)
    option = models.CharField(max_length = 6)
