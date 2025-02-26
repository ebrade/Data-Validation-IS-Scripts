import pandas as pd
from map_contract import MappContract

def add_default_fields(data):
        
        df =data

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY", "value": "RW"}, 
            {"column_name": "LE_BOOK", "value": "040"},
            {"column_name": "INTEREST_RATE_DR", "value": "0"}, 
            {"column_name": "INTEREST_RATE_DR", "value": "0"},
            {"column_name": "APR_RATE", "value": "0"}, 
            {"column_name": "INTEREST_RATE_METHOD", "value": "2"},
             
        ]

        for col in ADDITIONAL_COLUMNS:
            df[col["column_name"]] = col["value"]


        return df

data_acc = pd.read_csv('../Data/Source/ACCOUNT_ORACLE_DATA_OG.csv', dtype=str,sep='|')
# data_vision = pd.read_csv('../Data/Destination/CONTRACT_OG.csv', dtype=str,sep=',')
data_acc=data_acc[['CUSTOMER_ID','SUB_SEG','SECTOR', 'INDUSTRY', 'SEGMENT',
       'LEGAL_DOC_NAME']]
data = pd.read_csv('../Data/Source/CONTRACT_INFORMATION.csv', dtype=str,sep=',')

data['SETTLEMENT_DATE']=data['MATURITY_DATE']

data['SETTLEMENT_DATE'] = pd.to_datetime(data['SETTLEMENT_DATE'], format='%Y%m%d', errors='coerce')
data['MATURITY_DATE'] = pd.to_datetime(data['MATURITY_DATE'], format='%Y%m%d', errors='coerce')
data['START_DATE'] = pd.to_datetime(data['START_DATE'], format='%Y%m%d', errors='coerce')

data['TERM'] = (data['MATURITY_DATE'] - data['START_DATE']).dt.days


data = add_default_fields(data)

merged_data = data.merge(data_acc, on='CUSTOMER_ID', how='left')

map = MappContract(merged_data)

merged_data = (map
    .map_deal_type()
    .map_vision_SBU()
    .map_deal_sub_type()
    .get_mapped_dataframe()

)
merged_data.columns=merged_data.columns.str.replace('_',' ')
# print(merged_data)
print('test')