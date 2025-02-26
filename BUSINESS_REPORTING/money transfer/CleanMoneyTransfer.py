import pandas as pd
import numpy as np
from MappMoneyTransfer import MappMoneyTransfer

data = pd.read_csv('../Data/Source/MONEY_TRANSFER_ORACLE_DATA_OG.csv', dtype=str,sep='|')
data_vision = pd.read_csv('../Data/Destination/MONEY_TRANSFER_OG.csv', dtype=str,sep=',')
old_customer = pd.read_csv('../Data/Source/ALT_CUSTOMER_ID_ORACLE_DATA_OG.csv', dtype=str,sep='|')


def add_default_fields(data):
        
        df =data

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY", "value": "RW"}, 
            {"column_name": "LE_BOOK", "value": "040"},
             
        ]

        for col in ADDITIONAL_COLUMNS:
            df[col["column_name"]] = col["value"]


        return df

data = add_default_fields(data)

map = MappMoneyTransfer(data)

# # Add columns
mapped_data = (map
      .map_legal_doc_code()
      .map_remittence_type()
      .map_transaction_code()
      .map_customer_name()
    #   .map_other_id_type()
      .map_residents_flag()
      .get_mapped_dataframe() 
      )
mapped_data.columns = mapped_data.columns.str.replace('_', ' ')
old_customer.columns = old_customer.columns.str.replace('_', ' ')
data_vision.columns=data_vision.columns.str.upper()
mapped_data['BUSINESS DATE'] = pd.to_datetime(mapped_data['BUSINESS DATE'], format='%Y%m%d', errors='coerce')
mapped_data['SEQUENCE NUMBER']=mapped_data['RECID'].str[:-2]

mapped_data.to_csv('../DATA/Source/MONEY_TRANSFER.csv', index=False, sep=',')
data_vision.to_csv('../Data/Destination/MONEY_TRANSFER.csv', index=False, sep=',')

unique_T24 = set(mapped_data.columns).difference(data_vision.columns)

# # Columns unique to df2
unique_Vision = set(data_vision.columns).difference(mapped_data.columns)

print(unique_Vision)
print('======================================')
print(unique_T24)
print('======================================')
print(data_vision.columns)
