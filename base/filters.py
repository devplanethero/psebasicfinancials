import django_filters
from .models import Financials

class FinancialsFilter(django_filters.FilterSet):
    class Meta:
        model = Financials
        fields = {
            'reporting_period':['lt','gt'],
            'ticker__ticker':['iexact'],
            'ticker__type__type':['iexact'],
            'quarter':['iexact'],
            'year':['exact']
            }