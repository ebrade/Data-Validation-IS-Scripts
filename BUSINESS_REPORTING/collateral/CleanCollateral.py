import pandas as pd
import numpy as np
from MappCollateral import MappCollateral

data = pd.read_csv('../Data/Source/COLLATERAL_ORACLE_DATA_OG.csv', dtype=str,sep='|')
data_vision = pd.read_csv('../Data/Destination/COLLATERAL_OG.csv', dtype=str,sep=',')
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

map = MappCollateral(data)

# # Add columns
mapped_data = (map
      .map_collateral_type()
      .map_insured_status()
      .map_ownership_status()
      .get_mapped_dataframe() 
      )
mapped_data.columns = mapped_data.columns.str.replace('_', ' ')
old_customer.columns = old_customer.columns.str.replace('_', ' ')
mapped_data['COLLATERAL LAST VALUATION DATE'] = pd.to_datetime(mapped_data['COLLATERAL LAST VALUATION DATE'], format='%Y%m%d', errors='coerce')
mapped_data['COLLATERAL EXPIRY DATE'] = pd.to_datetime(mapped_data['COLLATERAL EXPIRY DATE'], format='%Y%m%d', errors='coerce')
mapped_data['INSURANCE EXPIRY DATE'] = pd.to_datetime(mapped_data['INSURANCE EXPIRY DATE'], format='%Y%m%d', errors='coerce')
mapped_data['DATE LAST MODIFIED'] = pd.to_datetime(mapped_data['DATE LAST MODIFIED'], format='%Y%m%d', errors='coerce')

mapped_data['COLLATERAL DISCOUNT AMT LCY']= pd.to_numeric(mapped_data['COLLATERAL AMOUNT LCY'], errors='coerce')*pd.to_numeric(mapped_data['COLLATERAL DISCOUNT RATE'], errors='coerce')/100
mapped_data['CONTRACT ID']=mapped_data['COLLATERAL ID']

merged_data = mapped_data.merge(old_customer, on='CUSTOMER ID', how='left')
merged_data["CUSTOMER ID"] = merged_data["ALT CUSTOMER"].fillna(merged_data["CUSTOMER ID"])

data_vision.loc[data_vision["CUSTOMER ID"].str.len() == 11, "CUSTOMER ID"] = data_vision["CUSTOMER ID"].str[:-5]
merged_data.to_csv('../DATA/Source/COLLATERAL.csv', index=False, sep=',')
data_vision.to_csv('../DATA/Destination/COLLATERAL.csv', index=False, sep=',')


unique_T24 = set(merged_data.columns).difference(data_vision.columns)

# # Columns unique to df2
unique_Vision = set(data_vision.columns).difference(merged_data.columns)

print(unique_Vision)
print('======================================')
print(unique_T24)
print('======================================')
print(data_vision.columns)
