from django.db import models
from django.urls import reverse
# Create your models here.
class Shelf(models.Model):
    shelf = models.CharField(max_length = 255, unique = True)

    def __str__(self):
        return self.shelf
    def get_absolute_url(self):
        return reverse("scanner:shelf_details", kwargs = {'pk':self.id})

class Scan(models.Model):
    shelf = models.CharField(max_length = 255, null = True)
    code = models.CharField(max_length = 255, null = True)
    code_manually = models.CharField(max_length = 255, null = True, blank = True)
    qty = models.IntegerField()

    def __str__(self):
        return self.code
