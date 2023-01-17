import pandas as pd
import re
from ...models import Financials, Company
from decimal import Decimal
import numpy
# from sqlalchemy import create_engine

from django.core.management.base import BaseCommand

def get_df(sheetName):
    sheet_id = "1mj38XJrBChSAtK9vJNmrCjySV0EHbQClo-r6C8UQYfg"
    sheet_name = sheetName.replace(" ","%20")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    return df


def clean_company_df(old_df, company):
    old_df = old_df.set_index(old_df.columns[0]) # use first column as index
    new_df = old_df.transpose() # transpose df
    new_df = new_df.reset_index(drop=False) 
    new_df.rename(columns = {new_df.columns[0]:'quarter_period'}, inplace = True)
    new_df['ticker'] = company
    
    # regex to find if year regex in quarter_period column
    yearRegex = re.compile(r'\d\d\d\d')
    new_df['period'] = new_df['quarter_period'].map(lambda x: yearRegex.search(x).group() if bool(yearRegex.search(x)) else 'quarter')
    
    # create new columns in df
    new_df['year'] = ''
    new_df['quarter'] = ''
    new_df['reporting_period'] = ''
    
    # 'year' column in df
    for i in range(0, len(new_df)):
        if new_df.period[i] != 'quarter':
            new_df.year[i] = new_df.period[i]
        elif i != 0:
            new_df.year[i] = new_df.year[i-1]
            
    # 'quarter column in df'
    for i in range(0, len(new_df)):
        if new_df.period[i] != 'quarter':
            new_df.quarter[i] = 'Q4'
        elif i != 0:
            
            if new_df.quarter[i-1] == 'Q1':
                new_df.quarter[i] = 'Q2'
            elif new_df.quarter[i-1] == 'Q2':
                new_df.quarter[i] = 'Q3'
            elif new_df.quarter[i-1] == 'Q3':
                new_df.quarter[i] = 'Q4'
            else:
                new_df.quarter[i] = 'Q1'
        
    # 'reporting period'
    for i in range(0, len(new_df)):
        if new_df.period[i] != 'quarter':
            new_df.reporting_period[i] = pd.to_datetime(new_df['year'][i]+'/12/31')
        else:
            if new_df.quarter[i] == 'Q1': 
                new_df.reporting_period[i] = pd.to_datetime(new_df['year'][i]+'/3/31')
            if new_df.quarter[i] == 'Q2': 
                new_df.reporting_period[i] = pd.to_datetime(new_df['year'][i]+'/6/30')
            if new_df.quarter[i] == 'Q3': 
                new_df.reporting_period[i] = pd.to_datetime(new_df['year'][i]+'/9/30')
            if new_df.quarter[i] == 'Q4': 
                new_df.reporting_period[i] = pd.to_datetime(new_df['year'][i]+'/12/31')

    # drop columns unnecessary:
    new_df = new_df.drop('quarter_period', axis=1)

    # replace column headers
    new_df.columns = new_df.columns.str.replace('-', '')
    new_df.columns = new_df.columns.str.replace(' ', '_')

    # clean blanks
    new_df = new_df.where(pd.notnull(new_df), None)
    
    # change column type
    new_df[new_df.columns[:26]]=new_df[new_df.columns[:26]].replace(',','',regex=True).fillna(0).astype('int64')
    return new_df


def consolidated_df():
# get all companies
    df = get_df("ALL COMPANIES")
    all_listed_companies = df[df.columns[0]].values.tolist()
    # sample 2GO
    company_df = get_df(all_listed_companies[0])
    # clean the df
    return clean_company_df(company_df, all_listed_companies[0])


class Command(BaseCommand):
    help = "A command to import google sheet financials to db"
 
    def handle(self, *args, **options):
        # importing it to sql database
        # engine = create_engine('sqlite:///db.sqlite3')
        # consolidated_df().to_sql(Financials._meta.db_table, con=engine, if_exists='append', index=False)

        df = get_df("ALL COMPANIES")
        all_listed_companies = df[df.columns[0]].values.tolist()

        for company in all_listed_companies:
            try:
                company_df = get_df(company)
                my_df = clean_company_df(company_df, company)

                for i in range(len(my_df)):
                    df_row = my_df.loc[i].tolist()

                    company_ticker = df_row[26]
                    ticker, created = Company.objects.get_or_create(ticker=company_ticker)
                    
                    Financials.objects.create(
                        Cash_and_Equivalents = Decimal(df_row[0].item()),
                        Current_Assets = Decimal(df_row[1].item()),
                        Fixed_Assets = Decimal(df_row[2].item()),
                        LongTerm_Investments = Decimal(df_row[3].item()),
                        Total_Assets = Decimal(df_row[4].item()),
                        Current_Debt = Decimal(df_row[5].item()),
                        Current_Liabilities = Decimal(df_row[6].item()),
                        LongTerm_Debt = Decimal(df_row[7].item()),
                        Total_Liabilities = Decimal(df_row[8].item()),
                        Equity = Decimal(df_row[9].item()),
                        Total_Equity = Decimal(df_row[10].item()),
                        Outstanding_Shares = Decimal(df_row[11].item()),
                        Revenue = Decimal(df_row[12].item()),
                        Operating_Income = Decimal(df_row[13].item()),
                        Income_on_Equity_Investments = Decimal(df_row[14].item()),
                        Net_Income = Decimal(df_row[15].item()),
                        Total_Net_Income = Decimal(df_row[16].item()),
                        Depreciation_and_Amortization = Decimal(df_row[17].item()),
                        Operating_Cash_Flow = Decimal(df_row[18].item()),
                        Capital_Expenditures = Decimal(df_row[19].item()),
                        Investing_Cash_Flow = Decimal(df_row[20].item()),
                        Total_Debt_Issued = Decimal(df_row[21].item()),
                        Total_Debt_Repaid = Decimal(df_row[22].item()),
                        Stock_Buyback = Decimal(df_row[23].item()),
                        Total_Dividends_Paid = Decimal(df_row[24].item()),
                        Financing_Cash_Flow = Decimal(df_row[25].item()),
                        ticker = ticker,
                        period = df_row[27],
                        year = df_row[28],
                        quarter = df_row[29],
                        reporting_period = df_row[30]
                    )
            except ValueError:
                pass # exclude e.g. FMETF