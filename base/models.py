from django.db import models

# Create your models here.
class Industry(models.Model):
    type = models.CharField(max_length=120)

    def __str__(self):
        return self.type

class Company(models.Model):
    ticker = models.CharField(max_length=120)
    name = models.CharField(max_length=120, null=True, blank=True)
    type = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, db_column='type')
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.ticker

class Financials(models.Model):
    Cash_and_Equivalents = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Current_Assets = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Fixed_Assets = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    LongTerm_Investments = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Total_Assets = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Current_Debt = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Current_Liabilities = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    LongTerm_Debt = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Total_Liabilities = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Equity = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Total_Equity = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Outstanding_Shares = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Revenue = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Operating_Income = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Income_on_Equity_Investments = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Net_Income = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Total_Net_Income = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Depreciation_and_Amortization = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Operating_Cash_Flow = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Capital_Expenditures = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Investing_Cash_Flow = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Total_Debt_Issued = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Total_Debt_Repaid = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Stock_Buyback = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Total_Dividends_Paid = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    Financing_Cash_Flow = models.DecimalField(decimal_places=2, max_digits=1000, null=True, blank=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, null= True)
    period = models.CharField(max_length=120, null= True)
    year = models.IntegerField(null=True)
    quarter = models.CharField(max_length=120, null= True)
    reporting_period = models.DateTimeField(null=True)
   

    class Meta:
        ordering = ['reporting_period'] # sort by oldest first


class Feedback(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(max_length=254)
    message = models.TextField(null=True, blank=True)
    submitted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__ (self):
        return self.email + ': ' + self.message[:50]