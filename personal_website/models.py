from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from django.db import models


@python_2_unicode_compatible
class GroceryVisit(models.Model):
    """
    A grocery visit includes all the items purchased at that trip, as well as the price and date.
    """
    price = models.IntegerField(default=1)
    date_added = models.DateTimeField('date added to list', default=timezone.now)

    def __str__(self):
        return "$%d purchased on %s" % (self.price, self.date_added)


@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField('date added to list', default=timezone.now)
    grocery_visit = models.ForeignKey(GroceryVisit, on_delete=models.CASCADE,
                                      default=None, blank=True, null=True)  # can be null before purchased

    def __str__(self):
        return self.name + " (%s)" % self.quantity
