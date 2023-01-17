from django.contrib import admin

# Register your models here.
from .models import (Industry, Company, Financials, Feedback)

admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(Financials)
admin.site.register(Feedback)