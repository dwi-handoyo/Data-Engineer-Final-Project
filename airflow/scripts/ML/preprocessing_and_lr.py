import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn import *

import time   
import logging

engine = create_engine("postgresql://postgres:admin@postgres-de9:5432/postgres")
#engine = create_engine("postgresql://postgres:admin@localhost:5445/postgres")

if __name__ == '__main__':

    # PREPROCESSING

    # Read the data
    train_data = pd.read_sql("select * from home_credit_default_risk_application_train", con=engine)
    test_data = pd.read_sql("select * from home_credit_default_risk_application_test", con=engine)
       
    # Drop columns with missing values (columns where null > 60%)  
    train_data = train_data.drop(train_data.columns[train_data.isnull().mean()>.6],axis=1)
    test_data = test_data.drop(test_data.columns[test_data.isnull().mean()>.6],axis=1)

    # load clean data to database
    try:
        insert_train = train_data.to_sql('home_credit_default_risk_application_train_clean', con=engine, if_exists='replace')
        insert_test = test_data.to_sql('home_credit_default_risk_application_test_clean', con=engine, if_exists='replace')
        logging.info(f'success insert data to table: home_credit_default_risk_application_train_clean, inserted {insert_train} data')
        logging.info(f'success insert data to table: home_credit_default_risk_application_test_clean, inserted {insert_test} data')
    except Exception as e:
        logging.info('Failed to insert data to table: home_credit_default_risk_application_train_clean')
        logging.error(e)

    #Data Splitting
    X = train_data.drop(columns=["TARGET"], axis=1)
    y = train_data["TARGET"]
    X_test = test_data

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3)

    # Numerical data
    num=X.select_dtypes(exclude='object').columns

    # Categorical data
    cat=X.select_dtypes(include='object').columns

    # Categorical data
    cat=X.select_dtypes(include='object').columns

    # SimpleImputer
    impute = SimpleImputer(strategy='median')
    Xnum = impute.fit_transform(X[num])

    # OneHotEncoder
    encode = OneHotEncoder()
    Xcat = encode.fit_transform(X[cat])

    # Modelling

    from sklearn.linear_model import LogisticRegression
    from imblearn.pipeline import Pipeline
    from sklearn.metrics import classification_report

    # Transformer Steps
    cat_trans = Pipeline([
    ('c_i', SimpleImputer(strategy="most_frequent")),
    ('c', OneHotEncoder(handle_unknown="ignore"))
    ])

    num_trans = Pipeline([
    ('n', SimpleImputer(strategy='median'))
    ])

    transformer = [
    ('c_t', cat_trans, cat),
    ('n_t', num_trans, num)
    ]

    # Logistic Regression
    model_lr = Pipeline([
    ('pre', ColumnTransformer(transformers=transformer)),
    ('model', LogisticRegression())
    ])

    model_lr.fit(X_train, y_train)

    #ML Model Report
    report = classification_report(y_test, model_lr.predict(X_test))
    #print(report)

    # Prediction
    y_predict = model_lr.predict(X_test)

    # Probability
    y_prob = model_lr.predict_proba(X_test)

    # ML Model Test
    # ML Model Result DataFrame

    ml_result = X_test[['SK_ID_CURR']]

    ml_result['prediction_target'] = y_predict.tolist()
    ml_result['status'] = "Not Accepted"

    status = ml_result['prediction_target'] >= 1
    ml_result.loc[status, 'status'] = 'Accepted'
    ml_result['probability'] =  y_prob.tolist()
  
    #print(ml_result)

    # Load prediction data to database
    try:
        res = ml_result.to_sql('home_credit_default_risk_application_ml_result', con=engine, if_exists='replace')
        logging.info(f'success insert data to table:  home_credit_default_risk_application_ml_result, inserted {res} data')
    except Exception as e:
        logging.info('Failed to insert data to table: home_credit_default_risk_application_ml_result')
        logging.error(e)


    