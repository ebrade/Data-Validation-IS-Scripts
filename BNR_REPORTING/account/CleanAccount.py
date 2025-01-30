import pandas as pd
import numpy as np
from MappAccount import MappAccount


data = pd.read_csv('../DATA/SOURCE/ACCOUNT_ORACLE_DATA_OG.csv', dtype=str,sep='|')
data_vision = pd.read_csv('../DATA/DESTINATION/ACCOUNT_OG.csv', dtype=str,sep=',')


def add_default_fields(data):
        
        df =data

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY", "value": "RW"}, 
            {"column_name": "LE_BOOK", "value": "040"},
            {"column_name": "INT RATE DR", "value": "0"}, 
            {"column_name": "INT RATE CR", "value": "0"},
            {"column_name": "ACCOUNT_CLOSING_DATE", "value": "01-JAN-1900"},
            {"column_name": "ACCOUNT_OWNERSHIP", "value": "O"},
            {"column_name": "CARD_SUBSCRIPTION", "value": "N"},
             
        ]

        for col in ADDITIONAL_COLUMNS:
            df[col["column_name"]] = col["value"]


        return df

data = add_default_fields(data)

map = MappAccount(data)

# # Add columns
mapped_data = (map
      .map_performance_class()
      .map_credit_category()
      .map_vision_sbu()
      .map_account_status()
      .map_account_type()
      .map_freeze_status()
      .map_public_sector_code()
      .map_institutional_sector_code()
      .get_mapped_dataframe() 
      )
mapped_data.columns = mapped_data.columns.str.replace('_', ' ')
mapped_data.rename(columns={'OPENING DATE':'ACCOUNT OPEN DATE','MOST RECENT DATE':'LAST TRANSACTION DATE'}, inplace=True)
mapped_data['Vision OUC'] = mapped_data['VISION OUC'].str[-5:]
# mapped_data["ALT ACC"] = mapped_data["ALT ACC"].str[:-3]
mapped_data["ACCOUNT NO"] = mapped_data["ALT ACC"].fillna(mapped_data["ACCOUNT NO"])
mapped_data['DATE LAST MODIFIED'] = pd.to_datetime(mapped_data['DATE LAST MODIFIED'], format='%Y%m%d', errors='coerce')

mapped_data.to_csv('../DATA/SOURCE/ACCOUNT.csv', index=False, sep=',')


data_vision.loc[data_vision["ACCOUNT NO"].str.len() == 18, "ACCOUNT NO"] = data_vision["ACCOUNT NO"].str[:-3]
data_vision.to_csv('../DATA/DESTINATION/ACCOUNT.csv', index=False, sep=',')

# unique_T24 = set(mapped_data.columns).difference(data_vision.columns)

# # # Columns unique to df2
# unique_Vision = set(data_vision.columns).difference(mapped_data.columns)

# print(unique_Vision)
# print('======================================')
# print(unique_T24)
# print('======================================')
# print(data_vision.columns)
