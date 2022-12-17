import pandas as pd
from sqlalchemy import create_engine
import logging

if __name__ == '__main__':
    engine = create_engine("postgresql://postgres:admin@postgres-de9:5432/postgres")
    #engine = create_engine("postgresql://postgres:admin@localhost:5445/postgres")

    # Extract Data
    companies = pd.read_sql(f"select * from companies", con=engine)
    dim_country = pd.read_sql(f"select * from dwh.dim_country", con=engine)
    
    # Transform Data
    cols = ['offices_state_code', 'offices_country_code']
    dim_state = companies.loc[:, [cols[0], cols[1]]]
    
    dim_state = dim_state[dim_state[cols[0]].notna()]
    dim_state = dim_state[dim_state[cols[0]] != '']
    dim_state = dim_state[dim_state[cols[1]].notna()]
    dim_state = dim_state[dim_state[cols[1]] != '']
 
    dim_state = dim_state.drop_duplicates(cols[0]) #cols[0] to distinct state_code  
    dim_state = dim_state.rename(columns={"offices_state_code":"state_code", "offices_country_code":"country_code"})
    dim_state.sort_values(by=['state_code'], inplace=True)
    dim_state = dim_state.merge(dim_country, on="country_code").reset_index()
    dim_state = dim_state.drop("country_code", axis=1)
    dim_state = dim_state.rename(columns={"index":"state_id"})
    dim_state['state_id'] += 1
    
    print(dim_state)
   
    # Load Data
    try:
        res = dim_state.to_sql('dim_state', con=engine, schema='dwh', index=False, if_exists='replace')
        print(f'success insert data to table: dim_state, inserted {res} data')
    except Exception as e:
        print('Failed to insert data to table: dim_state')
        print(f'ERROR: {e}')
