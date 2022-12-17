import pandas as pd
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine
import logging

engine = create_engine("postgresql://postgres:admin@postgres-de9:5432/postgres")
#engine = create_engine("postgresql://postgres:admin@localhost:5445/postgres")

if __name__ == '__main__':
    currencies = pd.read_sql(f"select * from rate_currency", con=engine)
    dim_currencies = pd.read_sql(f"select * from dwh.dim_currencies", con=engine)

    cols = ['currency_code', 'rate', 'timestamp']
    fct_currency_monthly = currencies.loc[:, [cols[0], cols[1], cols[2]]]
    
    # Convert the 'timestamp' column to a datetime object
    fct_currency_monthly[cols[2]] = pd.to_datetime(fct_currency_monthly[cols[2]])

    # Create a new column 'month' with the formatted month
    # Month format: "%Y-%m"
    fct_currency_monthly['month'] = fct_currency_monthly['timestamp'].dt.strftime("%Y-%m")
    fct_currency_monthly = fct_currency_monthly.merge(dim_currencies, on="currency_code")
    fct_currency_monthly = fct_currency_monthly.drop(columns=['timestamp', 'currency_code', 'currency_name'], axis=1)
    fct_currency_monthly = fct_currency_monthly.rename(columns={'rate':'monthly_rate_avg'}) 
    
    # Calculate the monthly average of the rates
    fct_currency_monthly_avg = fct_currency_monthly.groupby(['currency_id', 'month'])['monthly_rate_avg'].mean().reset_index()

    # Sort the dataframe by time
    fct_currency_monthly_avg = fct_currency_monthly_avg.sort_values('month')

    # Print the resulting dataframe
    print(fct_currency_monthly_avg)
  
    # Load to Data Warehouse (Schema: dwh)
    try:
        res = fct_currency_monthly_avg.to_sql('fct_currency_monthly', con=engine, schema='dwh', index=False, if_exists='replace')
        logging.info(f'success insert data to table: fct_currency_monthly, inserted {res} data')
    except Exception as e:
        logging.info('Failed to insert data to table: fct_currency_monthly')
        logging.error(e)
