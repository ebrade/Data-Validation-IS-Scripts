import re
import pandas as pd
from add_default_fields_customer import AddDefaultFields
from field_mapping_customer import CustomerMapping



class CleanCustomer():

    def add_default_fields_func(self):
        add_fields_obj = AddDefaultFields()
        add_fields_obj.add_default_fields()

    def sort_name_parts(self, name):
        if isinstance(name, str):
            parts = re.split(r'[ ,]+', name)
            sorted_parts = sorted(parts)
            return ' '.join(sorted_parts)
        return name
    
    def fields_mapping_func(self):
        data = pd.read_csv('../Data/Source/UPDATED_CUSTOMER.csv', dtype=str,sep='|')
        cust_map = CustomerMapping(data)
        mapped_data = (cust_map
            .map_vision_sbu()
            .map_vision_ouc()
            .map_place_of_birth()
            .map_legal_status()
            .map_inputter()
            .map_date_of_birth()
            .map_marital_status()
            .map_nextkin_id_type_in()
            .map_legal_doc_name()
            .map_bank_relation_relationshipe_type()
            .map_bank_relation_related_party()
            .map_residence_status()
            .map_education()
            .map_industry()
            .map_internet_banking_service()
            .map_mobile_banking_service()
            .map_gender()
            .map_occupation()
            .map_salutation()
            .map_legal_status()
            .map_surname()
            .map_perm_village()
            .map_customer_tin()
            .get_mapped_dataframe()
        )

        mapped_data.rename(columns={
            'NEXT_KIN_EMAIL' : 'NEXT_OF_KIN_EMAIL_ID',
            'NEXT_KIN_ID_NUMBER' : 'NEXT_OF_KIN_ID_NUMBER',
            'NEXT_KIN_TEL' : 'NEXT_OF_KIN_TELEPHONE',
            'GROUP_ID':'GROUP_NUMBER'
        }, inplace=True)

        mapped_data['CUSTOMER_NAME'] = mapped_data['FORENAME_1'].fillna(mapped_data['FORENAME_2'])
        mapped_data['CUSTOMER_OPEN_DATE'] = pd.to_datetime(mapped_data['CUSTOMER_OPEN_DATE'], format='%Y%m%d', errors='coerce')
        mapped_data['DATE_LAST_MODIFIED'] = pd.to_datetime(mapped_data['DATE_LAST_MODIFIED'].str[:6], format='%y%m%d').dt.strftime('%Y-%m-%d')
        mapped_data['CUSTOMER_NAME'] = mapped_data['CUSTOMER_NAME'].apply(self.sort_name_parts)
        mapped_data['NEXT_OF_KIN_NAME'] = mapped_data['NEXT_OF_KIN_NAME'].apply(self.sort_name_parts)
        mapped_data['NEXT_OF_KIN_TELEPHONE'] = mapped_data['NEXT_OF_KIN_TELEPHONE'].str.replace(r'^\+250', '0', regex=True)
        mapped_data['SOCIAL_ECONOMIC_CLASS'] = mapped_data.apply(
            lambda row: '9999' if row['VISION_SBU'] != 'RETL' 
            else '3' if row['VISION_SBU'] == 'RETL' 
            else row['SOCIAL_ECONOMIC_CLASS'], axis=1
        )
        mapped_data['CUSTOMER_TIN'] = mapped_data['NATIONAL_ID_NUMBER']
        mapped_data['COMM_VILLAGE'] = mapped_data['VILLAGE_ID'].fillna(mapped_data['COMM_VILLAGE']).fillna('OL01000001')
        mapped_data['PERM_COUNTRY'] = mapped_data['PERM_COUNTRY'].apply(lambda x: 'BE' if x == 'EU' else (str(x)[:2] if pd.notna(x) else 'RW'))

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
                'GENDER',
                'LEGAL_DOC_NAME',
                'SEGMENT'
            ], axis=1, inplace=True
        )
        mapped_data["CUSTOMER_ID"] = mapped_data["ALT_CUSTOMER"].fillna(mapped_data["CUSTOMER_ID"])
        mapped_data.to_csv('../Data/Source/CUSTOMER.csv', index=False, sep=',')

        vision_data = pd.read_csv('../Data/Destination/CUSTOMER_OG.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        vision_data.columns = vision_data.columns.str.replace(' ', '_').str.upper()
        vision_data['CUSTOMER_NAME'] = vision_data['CUSTOMER_NAME'].apply(self.sort_name_parts)
        vision_data['NEXT_OF_KIN_NAME'] = vision_data['NEXT_OF_KIN_NAME'].apply(self.sort_name_parts)
        vision_data['NEXT_OF_KIN_TELEPHONE'] = vision_data['NEXT_OF_KIN_TELEPHONE'].str.replace(r'^\+250', '0', regex=True)
        vision_data.loc[vision_data["CUSTOMER_ID"].str.len() == 11, "CUSTOMER_ID"] = vision_data["CUSTOMER_ID"].str[:-5]
        vision_data.to_csv('../Data/Destination/CUSTOMER.csv', index=False)




    def compare_columns(self):
        T24_DATA = pd.read_csv('../Data/Source/CUSTOMER.csv', dtype=str, sep=',', engine='python',encoding='latin1')
        VISION_DATA = pd.read_csv('../Data/Destination/CUSTOMER.csv', dtype=str, sep=',', engine='python',encoding='latin1')

        

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
    cleaner = CleanCustomer()
    result = cleaner.run()

