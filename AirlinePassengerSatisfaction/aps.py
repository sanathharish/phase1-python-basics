
import pandas as pd
import numpy as np
from utils.cleaning_utils import standerdize_column_names

# test = pd.read_csv(".\\RawData\\test.csv")

train = pd.read_csv(".\\RawData\\train.csv")

#Dropping unneeded metadata columns and convert float to int
test = train.drop(['Unnamed: 0','id'],axis=1,inplace=False)

test = standerdize_column_names(test)

test['arrival_delay_in_minutes'] = test['arrival_delay_in_minutes'].astype('Int64')

replace_map = {
    'satisfaction' : {'neutral or dissatisfied' : 'Unsatisfied', 'satisfied' : 'Satisfied'},
    'customer_type' : {'Loyal Customer':'Frequent Flyer','disloyal Customer':'Occasional Flyer'} 
}

test = test.replace(replace_map)
col_cat = ['gender', 'customer_type', 'age', 'type_of_travel', 'class','satisfaction']

test[col_cat]=test[col_cat].astype('category')

test['arrival_delay_in_minutes'].fillna(test['arrival_delay_in_minutes'].median(), inplace=True)

print(test.head())

# null_data = []
# for idx, delay in test['arrival_delay_in_minutes'].items():
#     if pd.isna(delay):
#         null_data.append({'index': idx, 'value': delay})

# print("Null values found:")
# for item in null_data:
#     print(f"Index: {item['index']}, Value: {item['value']}")

# null_indexes = test.index[test['arrival_delay_in_minutes'].isnull()]
# print(null_indexes)
# print(train.head())
# print(test.head(20))

#print(test.info())

# print(train.head())

# print(train.describe())

# print(train.info())

# print(train.shape)

# with open('.//RawData//columns_extract.txt','w') as f:
#        print(train.columns.tolist(), file = f)

print(test.isnull().sum())

# print(train[['Inflight wifi service',
#        'Departure/Arrival time convenient', 'Ease of Online booking',
#        'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
#        'Inflight entertainment', 'On-board service', 'Leg room service',
#        'Baggage handling', 'Checkin service', 'Inflight service',
#        'Cleanliness']].describe().to_csv('.//RawData//describe_output.csv'))

# print(train[['Inflight wifi service',
#        'Departure/Arrival time convenient', 'Ease of Online booking',
#        'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
#        'Inflight entertainment', 'On-board service', 'Leg room service',
#        'Baggage handling', 'Checkin service', 'Inflight service',
#        'Cleanliness']].describe())

# print(train[['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'satisfaction']].nunique())

# for col in train.select_dtypes(include='object').columns:
#     print(f'\n {col}:')
#     print(train[col].unique())

# summary = pd.DataFrame({
#        'dtype': train.dtypes,
#        'unique_count': train.nunique(),
#        'null_count': train.isnull().sum()
# })

# print(summary)

# print(train['Gate location'].nunique())
# print(train[['Gate location','satisfaction']].groupby('Gate location').size())


