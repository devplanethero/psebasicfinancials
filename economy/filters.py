import django_filters
from .models import EconomicIndicatorRecord

class EconomicsIndicatorRecordFilter(django_filters.FilterSet):
    class Meta:
        model = EconomicIndicatorRecord
        fields = {
            'country__name':['iexact'],
            'economic_indicator__title':['iexact'],
            'quarter':['iexact'],
            'year':['exact']
            }