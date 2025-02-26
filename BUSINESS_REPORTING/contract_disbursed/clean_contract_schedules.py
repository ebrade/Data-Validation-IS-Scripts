import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.BUSINESS_REPORTING.contract_disbursed.field_mapping_contract_schedules import ContractDisbursedMapping
import re
import pandas as pd
from is_data_validation.BUSINESS_REPORTING.contract_disbursed.add_default_fields_contract_disbursed import AddDefaultFields



class CleanBranchInfo():

    def add_default_fields_func(self):
        add_fields_obj = AddDefaultFields()
        add_fields_obj.add_default_fields()
    
    def fields_mapping_func(self):
        data = pd.read_csv('../Data/Source/UPDATED_CONTRACT_DISBURSED.csv', dtype=str,sep='|')
        
        contract_disbursed_map = ContractDisbursedMapping(data)
        mapped_data = (contract_disbursed_map
            .map_previous_disbursed_amt()
            .get_mapped_dataframe()
        )
        mapped_data.to_csv('../Data/Source/CONTRACT_DISBURSED.csv', index=False, sep=',')

        vision_data = pd.read_csv('../Data/Destination/CONTRACT_DISBURSED_OG.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        vision_data.columns = vision_data.columns.str.replace(' ', '_').str.upper()
        vision_data.to_csv('../Data/Destination/CONTRACT_DISBURSED.csv', index=False)

    def compare_columns(self):
        T24_DATA = pd.read_csv('../Data/Source/CONTRACT_DISBURSED.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        VISION_DATA = pd.read_csv('../Data/Destination/CONTRACT_DISBURSED.csv', dtype=str, sep=',', engine='python',encoding='latin1')

        vision_columns = set(VISION_DATA.columns)
        t24_columns = set(T24_DATA.columns)

        only_in_vision = vision_columns - t24_columns
        only_in_t24 = t24_columns - vision_columns

        print("======================== COLUMNS NOT IN T24 DATA =============================")
        print(only_in_vision)
        print("******************************************************************************")

        print("======================== COLUMNS NOT IN VISION DATA ==========================")
        print(only_in_t24)
        print("******************************************************************************")


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
    

        
