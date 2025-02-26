import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.BUSINESS_REPORTING.contract_schedule.field_mapping_contract_schedule import ContractScheduleMapping
import re
import pandas as pd
from is_data_validation.BUSINESS_REPORTING.contract_schedule.add_default_fields_contract_schedule import AddDefaultFields



class CleanBranchInfo():

    def add_default_fields_func(self):
        add_fields_obj = AddDefaultFields()
        add_fields_obj.add_default_fields()
    
    def fields_mapping_func(self):
        mapped_data = pd.read_csv('../Data/Source/UPDATED_CONTRACT_SCHEDULE.csv', dtype=str,sep='|')
        mapped_data['SCHEDULE_DATE'] = pd.to_datetime(mapped_data['SCHEDULE_DATE'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        mapped_data['PAYMENT_DATE'] = pd.to_datetime(mapped_data['PAYMENT_DATE'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        mapped_data['INT_AMOUNT_DUE_LCY'] = mapped_data['INT_AMOUNT_DUE_LCY'].fillna('0')
        mapped_data['INT_AMOUNT_PAID_LCY'] = mapped_data['INT_AMOUNT_PAID_LCY'].fillna('0')
        mapped_data['INT_AMOUNT_PAID_FCY'] = mapped_data['INT_AMOUNT_PAID_FCY'].fillna('0')
        mapped_data['OUTSTANDING_AMOUNT_LCY'] = mapped_data['OUTSTANDING_AMOUNT_LCY'].fillna('0')
        mapped_data['OUTSTANDING_AMOUNT_FCY'] = mapped_data['OUTSTANDING_AMOUNT_FCY'].fillna('0')
        mapped_data['PRINCIPAL_AMOUNT_DUE_FCY'] = mapped_data['PRINCIPAL_AMOUNT_DUE_FCY'].fillna('0')
        mapped_data['PRINCIPAL_AMOUNT_DUE_LCY'] = mapped_data['PRINCIPAL_AMOUNT_DUE_LCY'].fillna('0')
        mapped_data['PRINCIPAL_AMOUNT_PAID_LCY'] = mapped_data['PRINCIPAL_AMOUNT_PAID_LCY'].fillna('0')
        mapped_data['PRINCIPAL_AMOUNT_PAID_FCY'] = mapped_data['PRINCIPAL_AMOUNT_PAID_FCY'].fillna('0')
        mapped_data.to_csv('../Data/Source/CONTRACT_SCHEDULE.csv', index=False, sep=',')

        
        vision_data = pd.read_csv('../Data/Destination/CONTRACT_SCHEDULE_OG.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        vision_data.columns = vision_data.columns.str.replace(' ', '_').str.upper()
        vision_data['RECID'] = vision_data['CONTRACT_ID'] + "-" + vision_data['SCHEDULE_DATE'].str.replace('-', '').astype(str).str[:6]
        vision_data['INT_AMOUNT_DUE_LCY'] = vision_data['INT_AMOUNT_DUE_LCY'].str.replace('0000000000000000.000000', '0')
        vision_data['INT_AMOUNT_PAID_LCY'] = vision_data['INT_AMOUNT_PAID_LCY'].str.replace('0000000000000000.000000', '0')
        vision_data['INT_AMOUNT_PAID_FCY'] = vision_data['INT_AMOUNT_PAID_FCY'].str.replace('0000000000000000.000000', '0')
        vision_data['OUTSTANDING_AMOUNT_LCY'] = vision_data['OUTSTANDING_AMOUNT_LCY'].str.replace('0000000000000000.000000', '0')
        vision_data['OUTSTANDING_AMOUNT_FCY'] = vision_data['OUTSTANDING_AMOUNT_FCY'].str.replace('0000000000000000.000000', '0')
        vision_data['PRINCIPAL_AMOUNT_DUE_FCY'] = vision_data['PRINCIPAL_AMOUNT_DUE_FCY'].str.replace('0000000000000000.000000', '0')
        vision_data['PRINCIPAL_AMOUNT_DUE_LCY'] = vision_data['PRINCIPAL_AMOUNT_DUE_LCY'].str.replace('0000000000000000.000000', '0')
        vision_data['PRINCIPAL_AMOUNT_PAID_LCY'] = vision_data['PRINCIPAL_AMOUNT_PAID_LCY'].str.replace('0000000000000000.000000', '0')
        vision_data['PRINCIPAL_AMOUNT_PAID_FCY'] = vision_data['PRINCIPAL_AMOUNT_PAID_FCY'].str.replace('0000000000000000.000000', '0')
        vision_data.to_csv('../Data/Destination/CONTRACT_SCHEDULE.csv', index=False)

    def compare_columns(self):
        T24_DATA = pd.read_csv('../Data/Source/CONTRACT_SCHEDULE.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        VISION_DATA = pd.read_csv('../Data/Destination/CONTRACT_SCHEDULE.csv', dtype=str, sep=',', engine='python',encoding='latin1')

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
    

        
