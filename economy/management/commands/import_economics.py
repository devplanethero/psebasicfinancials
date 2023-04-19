import pandas as pd
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand
from ...models import Indicator, Country, EconomicIndicatorRecord
from decimal import Decimal


def generateDf():
    url = 'https://www.bsp.gov.ph/Statistics/Economic%20Indicators%20of%20Selected%20Countries/tab48_sas.aspx'
    req = Request(url = 'https://www.bsp.gov.ph/Statistics/Economic%20Indicators%20of%20Selected%20Countries/tab48_sas.aspx', headers = {'User-Agent': 'Mozilla/6.0'})
    webpage = urlopen(req).read()
    df = pd.read_html(webpage)[0]
    
    # get column headers
    raw_headers = df.iloc[[2]].values.tolist()[0]
    df.columns = raw_headers
    
    # removing unnecessary columns
    clean_df = df.iloc[:, [i for i,header in enumerate(df.columns) if type(header) != float or i < 4 and i != 0]]
    # removes NaN rows
    clean_df = clean_df.dropna(how='all').reset_index(drop=True)

    # renaming columns
    clean_df.columns.values[0] = "description"
    clean_df.columns.values[1] = "year"
    clean_df.columns.values[2] = "quarter"

    # cleaner year column
    quarters = ['Q1','Q2','Q3','Q4']

    for i in range(0, len(clean_df)):
        # get year from above row if quarter column is quarter
        if clean_df['quarter'][i] in quarters:
            if pd.isnull(clean_df['year'][i]): 
                clean_df['year'][i] = clean_df['year'][i-1]
            else:
                clean_df['year'][i] = clean_df['year'][i]
            
   #----------------GDP--------------------------
    gdp_df = clean_df[4:17].drop(['description'], axis=1) # remove description column
    gdp_df = gdp_df[gdp_df.quarter.isin(quarters)] # only rows with quarter
    gdp_df = gdp_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    gdp_df['economic_indicator'] = "GDP" # new column for economic_indicator type
    
    #----------------Inflation--------------------------
    inflation_df = clean_df[30:44].drop(['description'], axis=1)
    inflation_df = inflation_df[inflation_df.quarter.isin(quarters)] # only rows with quarter
    inflation_df = inflation_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    inflation_df['economic_indicator'] = "Inflation Rate" # new column for economic_indicator type
    
     #----------------Unemployment--------------------------
    unemployment_df = clean_df[44:58].drop(['description'], axis=1)
    unemployment_df = unemployment_df[unemployment_df.quarter.isin(quarters)] # only rows with quarter
    unemployment_df = unemployment_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    unemployment_df['economic_indicator'] = "Unemployment Rate" # new column for economic_indicator type
    
     #----------------Trade Balance--------------------------
    tradebal_df = clean_df[121:135].drop(['description'], axis=1)
    tradebal_df = tradebal_df[tradebal_df.quarter.isin(quarters)] # only rows with quarter
    tradebal_df = tradebal_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    tradebal_df['economic_indicator'] = "Trade Balance" # new column for economic_indicator type
    
     #----------------Net FDI--------------------------
    netFDI_df = clean_df[180:194].drop(['description'], axis=1)
    netFDI_df = netFDI_df[netFDI_df.quarter.isin(quarters)] # only rows with quarter
    netFDI_df = netFDI_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    netFDI_df['economic_indicator'] = "Net FDI" # new column for economic_indicator type
    
     #----------------TD Rate--------------------------
    timeDepositRate_df = clean_df[403:417].drop(['description'], axis=1)
    timeDepositRate_df = timeDepositRate_df[timeDepositRate_df.quarter.isin(quarters)] # only rows with quarter
    timeDepositRate_df = timeDepositRate_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    timeDepositRate_df['economic_indicator'] = "Time Deposit Rate" # new column for economic_indicator type
    
     #----------------Lending Rate--------------------------
    lendingRate_df = clean_df[417:431].drop(['description'], axis=1)
    lendingRate_df = lendingRate_df[lendingRate_df.quarter.isin(quarters)] # only rows with quarter
    lendingRate_df = lendingRate_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    lendingRate_df['economic_indicator'] = "Lending Rate" # new column for economic_indicator type

     #----------------TBill Rate--------------------------
    tBillRate_df = clean_df[431:445].drop(['description'], axis=1)
    tBillRate_df = tBillRate_df[tBillRate_df.quarter.isin(quarters)] # only rows with quarter
    tBillRate_df = tBillRate_df.melt(id_vars=["year", "quarter"],var_name="Country", value_name="Value") # convert columns per country into rows
    tBillRate_df['economic_indicator'] = "T-Bill Rate" # new column for economic_indicator type
    tBillRate_df
    
    # Combining the DataFrames
    consolidated_df = pd.concat([gdp_df, inflation_df, unemployment_df,tradebal_df, netFDI_df, timeDepositRate_df, lendingRate_df, tBillRate_df]).reset_index(drop=True)
    # New Period Column = Year + Quarter
    consolidated_df['period'] = consolidated_df['year'] + "_" + consolidated_df['quarter']
    
    # Cleaning Value Column:
    # Make str to float
    for i,value in enumerate(consolidated_df['Value']):
        try:
            consolidated_df['Value'][i] = float(value)
        except ValueError:
            consolidated_df['Value'][i] = float(0)
    
    return consolidated_df


class Command(BaseCommand):
    help = "A command to import from economic indicators from BSP website to Database"
 
    def handle(self, *args, **options):
        economics_df = generateDf()

        for i in range(len(economics_df)):
            row_values = economics_df.loc[i].tolist()
            
            economic_indicator, created_economic_indicator = Indicator.objects.get_or_create(title=row_values[4])
            country, created_country = Country.objects.get_or_create(name=row_values[2])

            updated_values = {'value':row_values[3]}
            EconomicIndicatorRecord.objects.update_or_create(
                economic_indicator = economic_indicator,
                country = country,
                year = row_values[0],
                quarter = row_values[1],
                period = row_values[5],
                defaults= updated_values
            )