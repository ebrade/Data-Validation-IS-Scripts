import pandas as pd
from add_default_fields_customer import AddDefaultFields
from field_mapping_customer import CustomerMapping



class CleanCustomer():

    def add_default_fields_func(self):
        add_fields_obj = AddDefaultFields()
        add_fields_obj.add_default_fields()
    
    def fields_mapping_func(self):

        data = pd.read_csv('./BUSINESSREPORT/DATA/SOURCE/UPDATED_CUSTOMER.csv', dtype=str,sep='|')
        cust_map = CustomerMapping(data)

        mapped_data = (cust_map
            .map_sub_seg()
            .map_company_book()
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
            .get_mapped_dataframe()
        )

    def compare_columns(self):
        T24_DATA = pd.read_csv('./BUSINESSREPORT/DATA/SOURCE/UPDATED_CUSTOMER.csv', dtype=str, sep='|')
        VISION_DATA = pd.read_csv('./BUSINESSREPORT/DATA/DESTINATION/CUSTOMER.csv', dtype=str, sep=',', engine='python',encoding='latin1')

        print("======================== T24 DATA COLUMNS =============================")
        print(T24_DATA.columns)
        print("=======================================================================")


        print("======================== VISION DATA COLUMNS ==========================")
        print(VISION_DATA.columns)
        print("=======================================================================")




    def run(self):
        # print("Running add_default_fields_func...")
        # self.add_default_fields_func()
        
        print("Running fields_mapping_func...")
        mapped_data = self.fields_mapping_func()

        self.compare_columns()
        

if __name__ == "__main__":
    cleaner = CleanCustomer()
    result = cleaner.run()
    