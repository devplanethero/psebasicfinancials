from django.urls import path
from . import views


app_name = 'base'

urlpatterns = [
    path('', views.homePage, name='home'),
    path('company/<str:ticker>/', views.companyPage, name='company'),
    path('company-list/', views.companyList, name='company-list'),
    path('about/', views.aboutPage, name='about'),

    path('company/<str:ticker>/export_csv', views.company_csv, name='company-csv'),
    path('api/get-companies/<str:q>/', views.getCompanies, name='get-companies')
]

