import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
import re
import pandas as pd
from is_data_validation.BUSINESS_REPORTING.bounce_cheque.add_default_fields_bounce_cheque import AddDefaultFields



class CleanBranchInfo():

    def add_default_fields_func(self):
        add_fields_obj = AddDefaultFields()
        add_fields_obj.add_default_fields()

        
    
    def fields_mapping_func(self):
        mapped_data = pd.read_csv('../Data/Source/UPDATED_BOUNCE_CHEQUE.csv', dtype=str,sep='|')

        mapped_data[['PREFIX', 'ACCOUNT_NO', 'CHEQUE_NO']] = mapped_data['RECID'].str.split('.', expand=True)
        mapped_data['CHEQUE_ISSUED_DATE'] = pd.to_datetime(mapped_data['CHEQUE_ISSUED_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
        mapped_data['BUSINESS_DATE'] = pd.to_datetime(mapped_data['BUSINESS_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
        
        mapped_data.drop(
            [
                'PREFIX'
            ], axis=1, inplace=True
        )

        old_account = pd.read_csv('../Data/Source/OLD_ACCOUNT_ORACLE_DATA.csv', dtype=str, sep='|')
        mapped_data = mapped_data.merge(old_account, on='ACCOUNT_NO', how='left')
        
        mapped_data['RECID'] = "CURR" + "." + mapped_data['ACCOUNT_NO'] + "." + mapped_data['CHEQUE_NO']
        mapped_data.to_csv('../Data/Source/BOUNCE_CHEQUE.csv', index=False, sep=',')

        vision_data = pd.read_csv('../Data/Destination/BOUNCE_CHEQUE_OG.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        vision_data.columns = vision_data.columns.str.replace(' ', '_')
        vision_data.loc[vision_data["ACCOUNT_NO"].str.len() == 18, "ACCOUNT_NO"] = vision_data["ACCOUNT_NO"].str[:-3]
        vision_data['RECID'] = "CURR" + "." + vision_data['ACCOUNT_NO'] + "." + vision_data['CHEQUE_NO']
        vision_data.to_csv('../Data/Destination/BOUNCE_CHEQUE.csv', index=False)

    def compare_columns(self):
        T24_DATA = pd.read_csv('../Data/Source/BOUNCE_CHEQUE.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        VISION_DATA = pd.read_csv('../Data/Destination/BOUNCE_CHEQUE.csv', dtype=str, sep=',', engine='python',encoding='latin1')

        vision_columns = set(VISION_DATA.columns)
        t24_columns = set(T24_DATA.columns)

        only_in_vision = vision_columns - t24_columns
        only_in_t24 = t24_columns - vision_columns

        print("======================== COLUMNS NOT IN T24 DATA =============================")
        print(only_in_vision)
        print("=======================================================================")

        print("======================== COLUMNS NOT IN VISION DATA ==========================")
        print(only_in_t24)
        print("=======================================================================")


    def run(self):
        # print("Running add_default_fields_func...")
        # self.add_default_fields_func()
        
        print("Running fields_mapping_func...")
        self.fields_mapping_func()
        
        # print("Running compare_columns_func...")
        # self.compare_columns()
        

if __name__ == "__main__":
    cleaner = CleanBranchInfo()
    result = cleaner.run()
    

        
