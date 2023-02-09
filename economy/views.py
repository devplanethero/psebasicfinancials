from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from .models import Indicator, Country, EconomicIndicatorRecord
from .filters import EconomicsIndicatorRecordFilter
from .serializer import EconomicIndicatorRecordSerializer, CountrySerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

def gdpPage(request):
    return render(request, 'economy/gdp.html')

def inflationPage(request):
    return render(request, 'economy/inflation.html')

def unemploymentPage(request):
    return render(request, 'economy/unemployment.html')

def tradeBalPage(request):
    return render(request, 'economy/tradebal.html')

def netFDIPage(request):
    return render(request, 'economy/netFDI.html')

def timeDepositPage(request):
    return render(request, 'economy/timedeposit.html')

def lendingPage(request):
    return render(request, 'economy/lending.html')

def tBillPage(request):
    return render(request, 'economy/t-bill.html')

class EconomicIndicatorRecordsListView(ListAPIView):
    queryset = EconomicIndicatorRecord.objects.all().order_by('period')
    serializer_class = EconomicIndicatorRecordSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EconomicsIndicatorRecordFilter

@api_view(['GET'])
def getCountries(request):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)
