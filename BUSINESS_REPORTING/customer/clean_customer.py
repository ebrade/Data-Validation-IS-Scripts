import pandas as pd
from add_default_fields_customer import AddDefaultFields
from field_mapping_customer import CustomerMapping



class CleanCustomer():

    def add_default_fields_func(self):
        add_fields_obj = AddDefaultFields()
        add_fields_obj.add_default_fields()
    
    def fields_mapping_func(self):

        data = pd.read_csv('../DATA/SOURCE/UPDATED_CUSTOMER.csv', dtype=str,sep='|')
        cust_map = CustomerMapping(data)

        mapped_data = (cust_map
            .map_sub_seg()
            .map_gender()
            .map_inputter()
            .map_date_of_birth()
            .map_marital_status()
            .map_nextkin_id_type_in()
            .map_residence_status()
            .map_bk_education()
            .map_industry()
            .map_bank_relation()
            .map_internet_banking_service()
            .map_mobile_banking_service()
            .map_occupation()
            .map_customer_status()
            .get_mapped_dataframe()
        )

        mapped_data.rename(columns={
            'NEXT_KIN_EMAIL' : 'NEXT_OF_KIN_EMAIL_ID',
            'NEXT_KIN_ID_NUMBER' : 'NEXT_OF_KIN_ID_NUMBER',
            'NEXT_KIN_TEL' : 'NEXT_OF_KIN_TELEPHONE',
            'GROUP_ID':'GROUP_NUMBER'
        }, inplace=True)

        mapped_data['CUSTOMER_NAME'] = mapped_data['FORENAME_1'] + ' ' + mapped_data['FORENAME_2']
        mapped_data['CUSTOMER_OPEN_DATE'] = pd.to_datetime(mapped_data['CUSTOMER_OPEN_DATE'], format='%Y%m%d', errors='coerce')

        mapped_data.drop(
            [
                'BK_EDUCATION', 
                'MOBILE_BANKING_SERVICE',
                'INPUTTER',
                'RESIDENCE_STATUS',
                'INTERNET_BANKING_SERVICE',
                'SUB_SEG',
                'NEXTKIN_ID_TYPE_IN',
                'INDUSTRY',
                'BANK_RELATION',
                'GENDER'
            ], axis=1, inplace=True
        )

   

        mapped_data.to_csv('./BUSINESSREPORT/DATA/SOURCE/CUSTOMER.csv', index=False, sep=',')

        vision_data = pd.read_csv('../DATA/DESTINATION/CUSTOMER.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        vision_data.columns = vision_data.columns.str.replace(' ', '_').str.upper()
        vision_data.to_csv('../DATA/DESTINATION/NEW_CUSTOMER.csv', index=False)




    def compare_columns(self):
        T24_DATA = pd.read_csv('../DATA/SOURCE/CUSTOMER.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        VISION_DATA = pd.read_csv('../DATA/DESTINATION/CUSTOMER.csv', dtype=str, sep=',', engine='python',encoding='latin1')

        

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
        
        # print("Running fields_mapping_func...")
        # mapped_data = self.fields_mapping_func()

        self.compare_columns()
        

if __name__ == "__main__":
    cleaner = CleanCustomer()
    result = cleaner.run()
    

        
