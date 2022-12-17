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
    fct_currency_daily = currencies.loc[:, [cols[0], cols[1], cols[2]]]
    
    # Convert the 'timestamp' column to a datetime object
    fct_currency_daily[cols[2]] = pd.to_datetime(fct_currency_daily[cols[2]])

    # Create a new column 'date' with the formatted date
    # Date format: "%Y-%m-%d"
    fct_currency_daily['date'] = fct_currency_daily['timestamp'].dt.strftime("%Y-%m-%d")
    fct_currency_daily = fct_currency_daily.merge(dim_currencies, on="currency_code")
    fct_currency_daily = fct_currency_daily.drop(columns=['timestamp', 'currency_code', 'currency_name'], axis=1)
    fct_currency_daily = fct_currency_daily.rename(columns={'rate':'daily_rate_avg'}) 
    # Calculate the daily average of the rates
    fct_currency_daily_avg = fct_currency_daily.groupby(['currency_id', 'date'])['daily_rate_avg'].mean().reset_index()

    # Sort the dataframe by time
    fct_currency_daily_avg = fct_currency_daily_avg.sort_values('date')

    # Print the resulting dataframe
    print(fct_currency_daily_avg)
    
    # Load to Data Warehouse (Schema: dwh) 
    try:
        res = fct_currency_daily_avg.to_sql('fct_currency_daily', con=engine, schema='dwh', index=False, if_exists='replace')
        logging.info(f'success insert data to table: fct_currency_daily, inserted {res} data')
    except Exception as e:
        logging.info('Failed to insert data to table: fct_currency_daily')
        logging.error(e)
