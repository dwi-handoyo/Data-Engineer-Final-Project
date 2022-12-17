import pandas as pd
from sqlalchemy import create_engine
import logging

if __name__ == '__main__':
    engine = create_engine("postgresql://postgres:admin@postgres-de9:5432/postgres")
    #engine = create_engine("postgresql://postgres:admin@localhost:5445/postgres")

    # Extract Data
    zips = pd.read_sql(f"select * from zips", con=engine)
    dim_state = pd.read_sql(f"select * from dwh.dim_state", con=engine)

    # Transform Data
    cols = ['state','city', 'zip']

    dim_city = zips.loc[:, [cols[0], cols[1], cols[2]]]
    dim_city = dim_city[dim_city[cols[0]].notna()]
    dim_city = dim_city[dim_city[cols[0]] != '']
    dim_city = dim_city[dim_city[cols[1]].notna()]
    dim_city = dim_city[dim_city[cols[1]] != '']    
    dim_city = dim_city[dim_city[cols[2]].notna()]
    dim_city = dim_city[dim_city[cols[2]] != '']
    
    dim_city = dim_city.drop_duplicates()
    dim_city = dim_city.rename(columns={"state":"state_code"})
    dim_city = dim_city.merge(dim_state, on="state_code").reset_index()
    dim_city = dim_city.drop(columns=["country_id", "state_code"], axis=1)
    dim_city = dim_city.rename(columns={"index":"city_id", "city":"city_name", "zip":"zip_code"})
    dim_city["city_id"] += 1
    print(dim_city)

    # Load Data
    try:
        res = dim_city.to_sql('dim_city', con=engine, schema='dwh', index=False, if_exists='replace')
        logging.info(f'success insert data to table: dim_city, inserted {res} data')
    except Exception as e:
        logging.info('Failed to insert data to table: dim_city')
        logging.error(e)
    