from django.urls import path
from . import views


app_name = 'base'

urlpatterns = [
    path('', views.homePage, name='home'),
    path('company/<str:ticker>/', views.companyPage, name='company'),
    path('company-list/', views.companyList, name='company-list'),
    path('about/', views.aboutPage, name='about'),
    path('leaderboards/', views.leaderboardsPage, name='leaderboards'),

    path('company/<str:ticker>/export_csv', views.company_csv, name='company-csv'),
    path('api/get-companies/<str:q>/', views.getCompanies, name='get-companies'),
    path('api/get-financials/', views.FinancialListView.as_view(), name='get-financials'),
    path('api/get-industries/', views.getIndustries, name='get-industries'),
]

