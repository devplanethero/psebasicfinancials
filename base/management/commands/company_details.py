from base.models import Company, Industry
from django.core.management.base import BaseCommand
import pandas as pd

class Command(BaseCommand):
    help = "A command to import google sheet financials to db"
 
    def handle(self, *args, **options):
        sheet_id = "1mj38XJrBChSAtK9vJNmrCjySV0EHbQClo-r6C8UQYfg"
        sheetName = "ALL COMPANIES"
        sheet_name = sheetName.replace(" ","%20")
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)

        for ticker, company_name, sector in zip(df.iloc[:,0], df.iloc[:,1], df.iloc[:,6]):
            # print(ticker, company_name, sector)

            # create name and type only for companies that exist in database
            try:
                company = Company.objects.get(ticker=ticker)
                industry, created = Industry.objects.get_or_create(type=sector)

                company.name = company_name
                company.type = industry
                company.save()
            except Company.DoesNotExist:
                pass