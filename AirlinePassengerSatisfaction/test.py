
import pandas as pd
import numpy as np
from utils.cleaning_utils import standerdize_column_names
from utils.semiauto_missing_data_handler import classify_feature_importance, handle_missing_data

# test = pd.read_csv(".\\RawData\\test.csv")

test = pd.read_csv(".\\RawData\\train.csv")

print(test.info())

# def check_missing_precent(test):
#     return (test.isnull().sum()/len(test)*100).sort_values(ascending=False)

# print(check_missing_precent(test))

# def check_missing(test):
#     return test.isnull().sum().sort_values(ascending=False)

# print(check_missing(test))

# target='satisfaction'
# corr_threshold=0.05
# numeric_cols = test.select_dtypes(include=['number']).columns
# if target in test.columns and test[target].dtype == 'object':
#         # Convert target to categorical codes for correlation
#         test['_target_encoded'] = test[target].astype('category').cat.codes
#         corr = test[numeric_cols].corrwith(test['_target_encoded']).abs().sort_values(ascending=False)
#         print(corr)