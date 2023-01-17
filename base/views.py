from django.shortcuts import render,redirect
from rest_framework.response import Response
from .models import Financials, Company, Industry, Feedback
from .forms import FeedbackForm
from django.db.models import Q # dynamic lookup
from .serializer import FinancialsSerializer, CompanySerializer
from rest_framework.decorators import api_view
from django.template.defaulttags import register
from datetime import datetime
from django.http import HttpResponse
import csv
from django.contrib import messages
# Create your views here.

def homePage(request):
    industries = Industry.objects.all()
    companies = Company.objects.all()
    context = {'industries':industries,
                'companies': companies,
                }
    return render(request, 'base/home.html', context)

def companyList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    companies = Company.objects.all()
    context = {'companies':companies,
                'q':q}
    return render(request, 'base/company_list.html', context)

def companyPage(request,ticker):
    period_status = request.GET.get('period') if request.GET.get('period') != None else 'year'
    f_date = '2010-12-05'
    from_date = datetime.strptime(f_date, "%Y-%m-%d").date()
    to_date = datetime.now()

    company = Company.objects.get(ticker=ticker)

    if period_status == 'year':
        financials = company.financials_set.exclude(Q(period__icontains='quarter')).filter(reporting_period__range=(from_date, to_date))
    else:
        financials = company.financials_set.filter(Q(period__icontains='quarter')).filter(reporting_period__range=(from_date, to_date))

    table_headers = ['']
    for period in financials:
        table_headers.append(period.reporting_period.strftime("%b %y").upper())
    
    # add TTM to end of current year
    if period_status == 'year':
        table_headers[-1] = table_headers[-1] + '/TTM'
    classification = {
        'Cash_and_Equivalents':'Cash and Equivalents' ,
        'Current_Assets':'Current Assets' ,
        'Fixed_Assets':'Fixed Assets' ,
        'LongTerm_Investments':'LongTerm Investments' ,
        'Total_Assets':'Total Assets' ,
        'Current_Debt':'Current Debt' ,
        'Current_Liabilities':'Current Liabilities' ,
        'LongTerm_Debt':'LongTerm Debt' ,
        'Total_Liabilities':'Total Liabilities' ,
        'Equity':'Equity' ,
        'Total_Equity':'Total Equity' ,
        'Outstanding_Shares':'Outstanding Shares' ,
        'Revenue':'Revenue' ,
        'Operating_Income':'Operating Income' ,
        'Income_on_Equity_Investments':'Income on Equity Investments' ,
        'Net_Income':'Net Income' ,
        'Total_Net_Income':'Total Net Income' ,
        'Depreciation_and_Amortization':'Depreciation and Amortization' ,
        'Operating_Cash_Flow':'Operating Cash Flow' ,
        'Capital_Expenditures':'Capital Expenditures' ,
        'Investing_Cash_Flow':'Investing Cash Flow' ,
        'Total_Debt_Issued':'Total Debt Issued' ,
        'Total_Debt_Repaid':'Total Debt Repaid' ,
        'Stock_Buyback':'Stock Buyback' ,
        'Total_Dividends_Paid':'Total Dividends Paid' ,
        'Financing_Cash_Flow':'Financing Cash Flow' ,
    }
    
            
    data = {}
    serializer = FinancialsSerializer(financials, many=True)
    field_names = [field.name for field in (Financials._meta.get_fields())]

    for field_name in field_names:
        values = []
        for row in serializer.data:
            values.append(row[field_name])
            data[field_name] = values

    # to get dictionary by key in html
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    context = {
        'company': company,
        'classification': classification,
        'table_headers': table_headers,
        'data':data,
        'period_status': period_status
    }
    return render(request, 'base/company.html', context)


# downloading CSV
def company_csv(request,ticker):
    company = Company.objects.get(ticker=ticker)
    financials = company.financials_set.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+ company.ticker +'.csv'

    # create a CSV writer:
    writer = csv.writer(response)

    writer.writerow(['reporting_period',
                'Cash_and_Equivalents',
                'Current_Assets',
                'Fixed_Assets',
                'LongTerm_Investments',
                'Total_Assets',
                'Current_Debt',
                'Current_Liabilities',
                'LongTerm_Debt',
                'Total_Liabilities',
                'Equity',
                'Total_Equity',
                'Outstanding_Shares',
                'Revenue',
                'Operating_Income',
                'Income_on_Equity_Investments',
                'Net_Income',
                'Total_Net_Income',
                'Depreciation_and_Amortization',
                'Operating_Cash_Flow',
                'Capital_Expenditures',
                'Investing_Cash_Flow',
                'Total_Debt_Issued',
                'Total_Debt_Repaid',
                'Stock_Buyback',
                'Total_Dividends_Paid',
                'Financing_Cash_Flow'
                    ])
    

    for row in financials:
        writer.writerow([
            row.reporting_period,
            row.Cash_and_Equivalents,
            row.Current_Assets,
            row.Fixed_Assets,
            row.LongTerm_Investments,
            row.Total_Assets,
            row.Current_Debt,
            row.Current_Liabilities,
            row.LongTerm_Debt,
            row.Total_Liabilities,
            row.Equity,
            row.Total_Equity,
            row.Outstanding_Shares,
            row.Revenue,
            row.Operating_Income,
            row.Income_on_Equity_Investments,
            row.Net_Income,
            row.Total_Net_Income,
            row.Depreciation_and_Amortization,
            row.Operating_Cash_Flow,
            row.Capital_Expenditures,
            row.Investing_Cash_Flow,
            row.Total_Debt_Issued,
            row.Total_Debt_Repaid,
            row.Stock_Buyback,
            row.Total_Dividends_Paid,
            row.Financing_Cash_Flow,
        ])
    
    return response

# Error 404 view
def handle_not_found(request, exception):
    return render(request, 'base/error404.html')

# API's
@api_view(['GET'])
def getCompanies(request, q):
    companies = Company.objects.filter(Q(name__icontains=q) |
                                        Q(ticker__icontains=q))
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


def aboutPage (request):
    feedback_form = FeedbackForm()
    context = {
        'feedback_form':feedback_form
    }

    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            print('form is valid')
            Feedback.objects.create(
                name = request.POST.get('name'),
                email = request.POST.get('email'),
                message = request.POST.get('message')
            )
            return redirect('base:about')

    return render(request, 'base/about.html', context)