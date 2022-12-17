import pandas as pd
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine
import logging

engine = create_engine("postgresql://postgres:admin@postgres-de9:5432/postgres")
#engine = create_engine("postgresql://postgres:admin@localhost:5445/postgres")

if __name__ == '__main__':

    df = pd.read_sql(f"select * from companies", con=engine)
    cols0 = ["offices_state_code"]
    cols1 = ["offices_state_code", "offices_city"]
    cols2 = ["offices_state_code", "offices_address1"]

    #All States in Data 
    df0 = pd.DataFrame(df, columns=cols0)
    df0 = df0[df0[cols0[0]].notna()]
    df0 = df0[df0[cols0[0]] != '']
    df0 = df0.groupby(cols0[0]).count()

    #Quantity of Cities in Each State
    df1 = pd.DataFrame(df, columns=cols1)
    df1 = df1[df1[cols1[0]].notna()]
    df1 = df1[df1[cols1[0]] != '']
    df1 = df1[df1[cols1[1]].notna()]
    df1 = df1[df1[cols1[1]] != '']
    df1 = df1.groupby(cols1[0]).count()

    #Quantity of Offices in Each State
    df2 = pd.DataFrame(df, columns=cols2)
    df2 = df2[df2[cols2[0]].notna()]
    df2 = df2[df2[cols2[0]] != '']
    df2 = df2[df2[cols2[1]].notna()]
    df2 = df2[df2[cols2[1]] != '']
    df2 = df2.groupby(cols2[0]).count()

    #Quantity of Cities and Offices at Each State
    fct_city_office_per_state = df0.merge(df1, how='outer', on=cols0[0])
    fct_city_office_per_state = fct_city_office_per_state.merge(df2, how='outer', on=cols0[0])
    fct_city_office_per_state = fct_city_office_per_state.fillna(0).reset_index()
    fct_city_office_per_state[cols1[1]] = fct_city_office_per_state[cols1[1]].apply(int)
    fct_city_office_per_state[cols2[1]] = fct_city_office_per_state[cols2[1]].apply(int)
    fct_city_office_per_state = fct_city_office_per_state.rename(columns={"offices_state_code":"state_code", "offices_city":"total_city", "offices_address1":"total_office"})
    print(fct_city_office_per_state)

    # Load to Data Warehouse (Schema: dwh)
    try:
        res = fct_city_office_per_state.to_sql('fct_city_office_per_state', con=engine, schema='dwh', index=False, if_exists='replace')
        print(f'success insert data to table: fct_agg_state, inserted {res} data')
    except Exception as e:
        print('Failed to insert data to table: fct_agg_state')
        print(f'ERROR: {e}')
