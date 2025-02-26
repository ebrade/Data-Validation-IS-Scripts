import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.BUSINESS_REPORTING.branch_info.field_mapping_branch_info import BranchInfoMapping
import re
import pandas as pd
from add_default_fields_branch_info import AddDefaultFields



class CleanBranchInfo():

    def add_default_fields_func(self):
        add_fields_obj = AddDefaultFields()
        add_fields_obj.add_default_fields()

    # def sort_name_parts(self, name):
    #     if isinstance(name, str):
    #         parts = re.split(r'[ ,]+', name)
    #         sorted_parts = sorted(parts)
    #         return ' '.join(sorted_parts)
    #     return name
    
    def fields_mapping_func(self):
        data = pd.read_csv('../Data/Source/UPDATED_BRANCH_INFO.csv', dtype=str,sep='|')

        data['VISION_OUC'] = data['COMPANY_CODE'].astype(str).str[-5:]
        data['BRANCH_OPEN_DATE'] = pd.to_datetime(data['BRANCH_OPEN_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
        data['BRANCH_CLOSE_DATE'] = pd.to_datetime(data['BRANCH_CLOSE_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
        
        branch_info_map = BranchInfoMapping(data)
        mapped_data = (branch_info_map
            .map_branch_status()
            .map_sub_branch_flag()
            .get_mapped_dataframe()
        )
        
        mapped_data.drop(
            [
                'COMPANY_CODE',
                'RECID'
            ], axis=1, inplace=True
        )

        mapped_data.to_csv('../Data/Source/BRANCH_INFO.csv', index=False, sep=',')

        vision_data = pd.read_csv('../Data/Destination/BRANCH_INFO_OG.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        vision_data.columns = vision_data.columns.str.replace(' ', '_')
        vision_data.to_csv('../Data/Destination/BRANCH_INFO.csv', index=False)



    def compare_columns(self):
        T24_DATA = pd.read_csv('../Data/Source/BRANCH_INFO.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        VISION_DATA = pd.read_csv('../Data/Destination/BRANCH_INFO.csv', dtype=str, sep=',', engine='python',encoding='latin1')

        

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
    

        
