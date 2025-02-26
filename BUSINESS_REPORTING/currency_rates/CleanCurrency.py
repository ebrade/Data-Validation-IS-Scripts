import pandas as pd
import numpy as np

data = pd.read_csv('../Data/Source/CURRENCY_RATES_ORACLE_DATA_OG.csv', dtype=str,sep='|')
data_vision = pd.read_csv('../Data/Destination/CURRENCY_RATES_OG.csv', dtype=str,sep=',')


def add_default_fields(data):
        
        df =data

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY", "value": "RW"}, 
            {"column_name": "LE_BOOK", "value": "040"},
             
        ]

        for col in ADDITIONAL_COLUMNS:
            df[col["column_name"]] = col["value"]


        return df

mapped_data = add_default_fields(data)
mapped_data.columns = mapped_data.columns.str.replace('_', ' ')

mapped_data['BUSINESS DATE'] = '20'+mapped_data['BUSINESS DATE'].str[:2]+mapped_data['BUSINESS DATE'].str[2:4]+mapped_data['BUSINESS DATE'].str[4:6]
mapped_data['BUSINESS DATE'] = pd.to_datetime(mapped_data['BUSINESS DATE'], format='%Y%m%d', errors='coerce')
mapped_data.to_csv('../DATA/Source/CURRENCY_RATES.csv', index=False, sep=',')

data_vision.columns=data_vision.columns.str.upper()
data_vision.to_csv('../DATA/Destination/CURRENCY_RATES.csv', index=False, sep=',')


unique_T24 = set(mapped_data.columns).difference(data_vision.columns)

# # Columns unique to df2
unique_Vision = set(data_vision.columns).difference(mapped_data.columns)

print(unique_Vision)
print('======================================')
print(unique_T24)
print('======================================')
print(data_vision.columns)
