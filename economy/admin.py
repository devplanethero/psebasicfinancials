from django.contrib import admin

# Register your models here.
from .models import (Indicator, Country, EconomicIndicatorRecord)

class EconomicIndicatorRecordAdmin(admin.ModelAdmin):
    search_fields = ['value']
    list_display = ['country', 'economic_indicator','period','value']
    list_filter = ['country', 'economic_indicator', 'year', 'quarter']


admin.site.register(Indicator)
admin.site.register(Country)
admin.site.register(EconomicIndicatorRecord, EconomicIndicatorRecordAdmin)
