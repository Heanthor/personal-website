from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from django.db import models


# Create your models here.
@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField('date added to list', default=timezone.now)

    def __str__(self):
        return self.name + " (%s)" % self.quantity
