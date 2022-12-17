import pandas as pd
from sqlalchemy import create_engine
import logging

if __name__ == '__main__':
    engine = create_engine("postgresql://postgres:admin@postgres-ds9:5432/postgres")
    #engine = create_engine("postgresql://postgres:admin@localhost:5445/postgres")
    # Extract Date
    currencies = pd.read_sql(f"select * from rate_currency", con=engine)
    #print(currencies['currency_code'])
    # Transform Data
    cols = ['currency_code', 'currency_name']
    
    dim_currencies = currencies[cols].groupby(cols).count().reset_index().reset_index()
    dim_currencies = dim_currencies.rename(columns={"index":"currency_id"})
    dim_currencies['currency_id'] += 1
    print(dim_currencies)
    
    # Load Data
    try:
        res = dim_currencies.to_sql('dim_currencies', con=engine, schema='dwh', index=False, if_exists='replace')
        logging.info(f'success insert data to table: dim_currencies, inserted {res} data')
    except Exception as e:
        logging.info('Failed to insert data to table: dim_currencies')
        logging.error(e)
