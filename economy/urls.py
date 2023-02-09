from django.urls import path
from . import views

app_name = 'economy'

urlpatterns = [
    path('api/economy_records/', views.EconomicIndicatorRecordsListView.as_view(), name='economy-records'),
    path('api/countries-list/', views.getCountries, name='get-countries'),
    path('gdp/', views.gdpPage, name='gdp'),
    path('inflation/', views.inflationPage, name='inflation'),
    path('unemployment/', views.unemploymentPage, name='unemployment'),
    path('tradebalance/', views.tradeBalPage, name='tradebal'),
    path('netfdi/', views.netFDIPage, name='netFDI'),
    path('timedeposit/', views.timeDepositPage, name='timedeposit'),
    path('lending/', views.lendingPage, name='lending'),
    path('t-bill/', views.tBillPage, name='tbill'),
]