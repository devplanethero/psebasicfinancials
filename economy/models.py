from django.db import models

# Create your models here.
class Indicator(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

class Country(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class EconomicIndicatorRecord(models.Model):
    economic_indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    year = models.IntegerField(null=True)
    quarter = models.CharField(max_length=120, null= True)
    period = models.CharField(max_length=120, null= True)
    value = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)

    def __str__(self):
        return self.country.name + " - " + self.economic_indicator.title + " - " + self.period
