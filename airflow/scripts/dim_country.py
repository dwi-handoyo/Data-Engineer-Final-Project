import pandas as pd
from sqlalchemy import create_engine
import logging

if __name__ == '__main__':
    engine = create_engine("postgresql://postgres:admin@postgres-de9:5432/postgres")
    #engine = create_engine("postgresql://postgres:admin@localhost:5445/postgres")

    # Extract Data
    companies = pd.read_sql(f"select * from companies", con=engine)
    
    # Transform Data
    cols = ['offices_country_code']
    filt_empty_country = companies['offices_country_code'] != ''
    dim_country = companies[filt_empty_country][cols].groupby(cols).count().reset_index().reset_index()
    dim_country = dim_country.rename(columns={"index":"country_id", "offices_country_code":"country_code"})
    dim_country = dim_country[dim_country.country_code != '']
    dim_country['country_id'] += 1
    print(dim_country)

    # Load Data
    try:
        res = dim_country.to_sql('dim_country', con=engine, schema='dwh', index=False, if_exists='replace')
        logging.info(f'success insert data to table: dim_country, inserted {res} data')
    except Exception as e:
        logging.info('Failed to insert data to table: dim_country')
        logging.error(e)
