import numpy as np
from datetime import datetime
import pandas as pd

class CustomerMapping():
    def __init__(self, df):
        self.df = df

    def map_vision_sbu(self):
        self.df['SUB_SEG'] = pd.to_numeric(self.df['SUB_SEG'], errors='coerce')
        conditions = [
            self.df['LEGAL_DOC_NAME'].isin(['NGO', 'NPO']),
            self.df['LEGAL_DOC_NAME'].isin(['ASSOCIATION', 'COOPERATIVE', 'REFERENCE.LETTER', 'IBIMINA']),
            self.df['LEGAL_DOC_NAME'].isin(['EMBASSY']),
            self.df['LEGAL_DOC_NAME'].isin([
                'NATIONAL.ID', 'NATIONAL.ID.FOR', 'PASSPORT', 'GUARDIAN', 
                'EAC.ID', 'GUARDIAN.ID', 'CEPGL.ID', 'NATIONAL.ID.REF', 'CHILD.ID'
            ]),
            self.df['SUB_SEG'].isin([40, 41, 42, 43, 22, 23]),
            self.df['SUB_SEG'] == 20,
            self.df['SUB_SEG'].isin([21, 25, 30]),
            self.df['SUB_SEG'] == 24,
            self.df['SUB_SEG'].isin([50, 51, 52, 53]),
            self.df['SEGMENT'] == 1,
            self.df['SUB_SEG'].isna() & (self.df['SECTOR'] != '1000'),
            self.df['SUB_SEG'].isna() & (self.df['SECTOR'] == '1000')
        ]
        
        values = [
            'NGO', 'SAGRP', 'OTHER', 'RETL', 
            'LRGOTHR', 'MCEOTHR', 'MEDOTHR', 'SMLOTHR', 'LRGOTHR', 'RETL','MEDOTHR', 'RETL'
        ]
        self.df['VISION_SBU'] = np.select(conditions
            ,values, default=None)
        return self

    def map_gender(self):
        conditions = [
            self.df['GENDER'] == 'MALE',
            self.df['GENDER'] == 'FEMALE',
            self.df['VISION_SBU'] != 'RETL',
            self.df['SECTOR'] == '1003'
        ]
       
        values = ['M', 'F', 'C', 'C']
        self.df['CUSTOMER_GENDER'] = np.select(conditions, values, default=self.df['GENDER'])
        return self

    def map_vision_ouc(self):
        self.df['VISION_OUC'] = self.df['COMPANY_BOOK'].astype(str).str[-5:]

        conditions = [
            self.df['VISION_OUC'] == '10049',
            self.df['VISION_OUC'] == '20001'
        ]

        values = ['10022', '10001']
        self.df['VISION_OUC'] = np.select(conditions, values, default=self.df['VISION_OUC'])
        return self

    def map_perm_village(self):
        self.df['PERM_VILLAGE'] = np.where(
            self.df['VILLAGE_ID'].notna(), self.df['VILLAGE_ID'],
            np.where(self.df['COMM_VILLAGE'].notna(), self.df['COMM_VILLAGE'], 'OL01000001')
        )

        self.df['PERM_VILLAGE'] = np.where(
            self.df['PERM_VILLAGE'].isin(['OL9999999', 'OL99999999']), 'OL01000001', self.df['PERM_VILLAGE']
        )
        return self

    def map_place_of_birth(self):
        self.df['PLACE_OF_BIRTH'] = np.where(
            self.df['NATIONALITY'] != 'RW', 
            self.df['NATIONALITY'], 
            self.df['VILLAGE_ID'].fillna(self.df['COMM_VILLAGE'])
        )

        conditions = [
            self.df['PLACE_OF_BIRTH'] == 'EU',
            self.df['PLACE_OF_BIRTH'].isin(['OL9999999', 'OL99999999'])
        ]
        
        values = [
            'BE',
            'OL01000001'
        ]

        self.df['PLACE_OF_BIRTH'] = np.select(conditions, values, default=self.df['PLACE_OF_BIRTH'])
        return self


    def map_legal_status(self):
        conditions = [
            self.df['CUSTOMER_STATUS'].isin(['8']),
            self.df['CUSTOMER_STATUS'].isin(['9']),
            self.df['CUSTOMER_STATUS'].isin(['10']),
            self.df['CUSTOMER_STATUS'].isin(['12']),
            self.df['CUSTOMER_STATUS'].isin(['13']),
            self.df['CUSTOMER_STATUS'].isin(['50']),
            self.df['CUSTOMER_STATUS'].isin(['60']),
        ]

        values = ['2', '3', '4', '6', '7', '2', '4']
        self.df['LEGAL_STATUS'] = np.select(conditions, values, default=self.df['CUSTOMER_STATUS'])
        return self

    def map_inputter(self):
        conditions = [
            self.df['INPUTTER'].isin(['ESBUSER']),
        ]

        values = ['MOB']
        self.df['ACCOUNT_OPENING_MODE'] = np.select(conditions, values, default='OTC')
        return self

    def map_date_of_birth(self):
        self.df['DATE_OF_BIRTH'] = pd.to_datetime(self.df['DATE_OF_BIRTH'], format='%Y%m%d', errors='coerce')
        self.df['DATE_OF_BIRTH'] = self.df['DATE_OF_BIRTH'].fillna(pd.to_datetime('19000101', format='%Y%m%d'))
        self.df.loc[self.df['DATE_OF_BIRTH'] < pd.to_datetime('1900-01-01'), 'DATE_OF_BIRTH'] = pd.to_datetime('19000101', format='%Y%m%d')
        return self

    def map_date_of_birth(self):
        self.df['DATE_OF_BIRTH'] = pd.to_datetime(self.df['DATE_OF_BIRTH'], format='%Y%m%d', errors='coerce')
        self.df['DATE_OF_BIRTH'] = self.df['DATE_OF_BIRTH'].fillna(
            pd.to_datetime(self.df['BIRTH_INCORP_DATE'], errors='coerce')
        )
        self.df.loc[self.df['BIRTH_INCORP_DATE'] == '1900-01-01', 'DATE_OF_BIRTH'] = pd.to_datetime(
            self.df['LEGAL_ISS_DATE'], errors='coerce'
        )
        self.df['DATE_OF_BIRTH'] = self.df['DATE_OF_BIRTH'].fillna(
            pd.to_datetime(self.df['LEGAL_ISS_DATE'], errors='coerce')
        )
        self.df.loc[self.df['DATE_OF_BIRTH'] < pd.to_datetime('1900-01-01'), 'DATE_OF_BIRTH'] = pd.to_datetime('1900-01-01')
        return self

    def map_customer_tin(self):
        self.df['CUSTOMER_TIN'] = self.df.apply(
            lambda row: str(row['CUSTOMER_TIN'])[:10] if row['VISION_SBU'] != 'RETL' else 'NA', 
            axis=1
        )
        return self

    def map_marital_status(self):
            conditions = [
                self.df['MARITAL_STATUS'].isin(['MARRIED']),
                self.df['MARITAL_STATUS'].isin(['WIDOWED']),
                self.df['MARITAL_STATUS'].isin(['SEPARATED']),
                self.df['MARITAL_STATUS'].isin(['DIVORCED']),
                self.df['MARITAL_STATUS'].isin(['SINGLE']),
            ]
            values = ['001', '003', '004', '005', '006']
            self.df['MARITAL_STATUS'] = np.select(conditions, values, default='NA')
            return self

    def map_nextkin_id_type_in(self):
            conditions = [
                self.df['NEXTKIN_ID_TYPE_IN'].isin(['NATIONAL.ID', 'NATIONAL.ID.REF']),
                self.df['NEXTKIN_ID_TYPE_IN'].isin(['PASSPORT']),
                self.df['NEXTKIN_ID_TYPE_IN'].isin(['EAC.ID', 'GUARDIAN']),
            ]
            values = [2, 4, 7]
            self.df['NEXT_OF_KIN_ID_TYPE'] = np.select(conditions, values, default='NULL')
            return self

    def map_legal_doc_name(self):
            conditions = [
                self.df['LEGAL_DOC_NAME'].isin(['ASSOCIATION', 'REFERENCE.LETTER', 'IBIMINA']),
                self.df['LEGAL_DOC_NAME'].isin(['CEPGL.ID', 'EAC.ID', 'NATIONAL.ID.FOR']),
                self.df['LEGAL_DOC_NAME'].isin(['COMPANY', 'COOPERATIVE', 'FINANCIAL', 'NGO', 'NPO']),
                self.df['LEGAL_DOC_NAME'].isin(['EMBASSY', 'PUBLIC']),
                self.df['LEGAL_DOC_NAME'].isin(['CHILD.ID']),
                self.df['LEGAL_DOC_NAME'].isin(['GUARDIAN', 'GUARDIAN.ID', 'NATIONAL.ID']),
                self.df['LEGAL_DOC_NAME'].isin(['PASSPORT']),
                self.df['LEGAL_DOC_NAME'].isin(['NATIONAL.ID.REF'])
            ]

            values = [9, 5, 6, 7, 8, 2, 4, 3]
            self.df['NATIONAL_ID_TYPE'] = np.select(conditions, values, default=9)
            return self

    def map_bank_relation_relationshipe_type(self):
            conditions = [
                self.df['BANK_RELATION'].isin(['NON', 'NO RELATION']),
                self.df['BANK_RELATION'].isna()
            ]

            values = [25, 25]
            self.df['RELATIONSHIP_TYPE'] = np.select(conditions, values, default=23)
            return self

    def map_bank_relation_related_party(self):
            conditions = [
                self.df['BANK_RELATION'].isin(['DIR']),
                self.df['BANK_RELATION'].isin(['NON', 'NO RELATION']),
                self.df['BANK_RELATION'].isin(['STAFF']),
                self.df['BANK_RELATION'].isin(['MGT'])
            ]

            values = ['DIR', 'NON', 'STAFF', 'MGT']
            self.df['RELATED_PARTY'] = np.select(conditions, values, default='NON')
            return self

    def map_residence_status(self):
            conditions = [
                self.df['RESIDENCE_STATUS'].isin(['PROPERTY.OWNER', 'NON.TENANT'])
            ]

            values = ['O']
            self.df['COMM_RESIDENCE_TYPE'] = np.select(conditions, values, default='T')
            return self

    def map_education(self):
            self.df['BK_EDUCATION'] = pd.to_numeric(self.df['BK_EDUCATION'], errors='coerce')

            self.df['EDUCATION'] = np.where(
                (self.df['BK_EDUCATION'] >= 1) & (self.df['BK_EDUCATION'] <= 8),
                self.df['BK_EDUCATION'], 
                3
            )
            return self

    def map_industry(self):
        industry_mapping = {
            1: 'A', 2: 'B', 3: 'C', 4: 'D', 6: 'F', 7: 'G',
            8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M',
            14: 'N', 16: 'O', 17: 'P', 18: 'Q', 19: 'R', 20: 'S',
            21: 'T', 22: 'U', 23: 'E'
        }
        
        self.df['INDUSTRY'] = self.df['INDUSTRY'].astype(int, errors='ignore')
        self.df['ECONOMIC_SECTOR_CODE'] = self.df['INDUSTRY'].map(industry_mapping).fillna('NA')
        return self

    def map_internet_banking_service(self):
        conditions = [
            self.df['INTERNET_BANKING_SERVICE'].isin(['YES']),
        ]

        values = ['Y']
        self.df['INTERNET_BANKING_SUBSCRIPTION'] = np.select(conditions, values, default='N')
        return self

    def map_mobile_banking_service(self):
        conditions = [
            self.df['MOBILE_BANKING_SERVICE'].isin(['YES']),
        ]

        values = ['Y']
        self.df['MOBILE_BANKING_SUBSCRIPTION'] = np.select(conditions, values, default='N')
        return self

    def map_occupation(self):
        conditions = [
            self.df['VISION_SBU'] != 'RETL', 
            (self.df['VISION_SBU'] == 'RETL') & (self.df['OCCUPATION'].astype(str).str.len() < 3)
        ]
        
        values = ['9999','5169']
        self.df['OCCUPATION'] = np.select(conditions, values, default=self.df['OCCUPATION'])
        return self
    
    def map_surname(self):
        self.df['SURNAME'] = np.where(self.df['VISION_SBU'] != 'RETL', self.df['SHORT_NAME'], self.df['SURNAME'])
        return self

    def map_salutation(self):
        self.df['SALUTATION'] = self.df['SALUTATION'].fillna('NA')

        conditions = [
            (self.df['VISION_SBU'] == 'RETL') & (self.df['CUSTOMER_GENDER'] == 'NA') & (self.df['SALUTATION'] == 'NA'),
            (self.df['VISION_SBU'] == 'RETL') & (self.df['SALUTATION'] == 'NA') & (self.df['CUSTOMER_GENDER'] == 'M'),
            (self.df['VISION_SBU'] == 'RETL') & (self.df['SALUTATION'] == 'NA') & (self.df['CUSTOMER_GENDER'] == 'F'),
            (self.df['CUSTOMER_GENDER'] == 'F') & (self.df['SALUTATION'] == 'MR'),
            (self.df['CUSTOMER_GENDER'] == 'M') & (~self.df['SALUTATION'].isin(['MR'])),
            (self.df['CUSTOMER_GENDER'] == 'C') & (~self.df['SALUTATION'].isin(['CORP'])),
            self.df['SECTOR'] == '1003'
        ]

        values = ['MR', 'MR', 'MRS', 'MRS', 'MR', 'CORP', 'CORP']
        self.df['SALUTATION'] = np.select(conditions, values, default=self.df['SALUTATION'])
        return self
    
    def get_mapped_dataframe(self):
        return self.df