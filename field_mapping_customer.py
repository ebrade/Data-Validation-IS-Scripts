import numpy as np
from datetime import datetime
import pandas as pd

class CustomerMapping():
    def __init__(self, df):
        self.df = df

    def map_sub_seg(self):
        conditions = [
            self.df['SUB_SEG'].isin([10, 11, 12]),
            self.df['SUB_SEG'].isin([43]),
            self.df['SUB_SEG'].isin([41]),
            self.df['SUB_SEG'].isin([23, 42]),
            self.df['SUB_SEG'].isin([22]),
            self.df['SUB_SEG'].isin([30]),
            self.df['SUB_SEG'].isin([20, 24, 25]),
            self.df['SUB_SEG'].isin([40]),
            self.df['SUB_SEG'].isin([21]),
        ]

        values = ['RETL', 'INST', 'LRGOTHR', 'LRGCOMP', 'MEDCOMP', 'OTHER', 'MCECOMP', '', 'SMLCOMP']
        self.df['VISION_SBU'] = np.select(conditions, values, default='NA')
        return self

    def map_company_book(self):
        conditions = [
            self.df['SUB_SEG'].isin([10, 11, 12]),
            self.df['SUB_SEG'].isin([43]),
            self.df['SUB_SEG'].isin([41]),
            self.df['SUB_SEG'].isin([23, 42]),
            self.df['SUB_SEG'].isin([22]),
            self.df['SUB_SEG'].isin([30]),
            self.df['SUB_SEG'].isin([20, 24, 25]),
            self.df['SUB_SEG'].isin([40]),
            self.df['SUB_SEG'].isin([21]),
        ]

        values = ['RETL', 'INST', 'LRGOTHR', 'LRGCOMP', 'MEDCOMP', 'OTHER', 'MCECOMP', '', 'SMLCOMP']
        self.df['VISION_SBU'] = np.select(conditions, values, default='NA')
        return self

    def map_gender(self):
        conditions = [
            self.df['GENDER'].isin(['MALE']),
            self.df['GENDER'].isin(['FEMALE']),
        ]

        values = ['M', 'F']
        self.df['CUSTOMER_GENDER'] = np.select(conditions, values, default='NA')
        return self

    def map_inputter(self):
        conditions = [
            self.df['INPUTTER'].isin(['ESBUSER']),
        ]

        values = ['MOB']
        self.df['ACCOUNT_OPENING_MODE'] = np.select(conditions, values, default='OTC')
        return self

    def map_date_of_birth(self):
        conditions = [
            self.df['DATE_OF_BIRTH'] < '01-JAN-1900',
        ]
        values = ['19000101']
        self.df['DATE_OF_BIRTH'] = np.select(conditions, values)
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
            self.df['NEXTKIN_ID_TYPE_IN'].isin(['EAC.ID']),
            self.df['NEXTKIN_ID_TYPE_IN'].isin(['GUARDIAN'])
        ]

        values = [2, 4, 7, 7]
        self.df['NEXT_OF_KIN_ID_TYPE'] = np.select(conditions, values, default=7)
        return self

    def map_residence_status(self):
        conditions = [
            self.df['RESIDENCE_STATUS'].isin(['PROPERTY.OWNER', 'NON.TENANT'])
        ]

        values = ['O']
        self.df['COMM_RESIDENCE_TYPE'] = np.select(conditions, values, default='T')
        return self


    def map_bk_education(self):
        self.df['BK_EDUCATION'] = pd.to_numeric(self.df['BK_EDUCATION'], errors='coerce')

        conditions = [
            (self.df['BK_EDUCATION'] >= 1) & (self.df['BK_EDUCATION'] <= 8)
        ]

        values = [self.df['BK_EDUCATION']]
        self.df['EDUCATION'] = np.select(conditions, values, default=3)
        return self


    def map_industry(self):
        conditions = [
            self.df['INDUSTRY'].isin([1]),
            self.df['INDUSTRY'].isin([2]),
            self.df['INDUSTRY'].isin([3]),
            self.df['INDUSTRY'].isin([4]),
            self.df['INDUSTRY'].isin([6]),
            self.df['INDUSTRY'].isin([7]),
            self.df['INDUSTRY'].isin([8]),
            self.df['INDUSTRY'].isin([9]),
            self.df['INDUSTRY'].isin([10]),
            self.df['INDUSTRY'].isin([11]),
            self.df['INDUSTRY'].isin([12]),
            self.df['INDUSTRY'].isin([13]),
            self.df['INDUSTRY'].isin([14]),
            self.df['INDUSTRY'].isin([16]),
            self.df['INDUSTRY'].isin([17]),
            self.df['INDUSTRY'].isin([18]),
            self.df['INDUSTRY'].isin([19]),
            self.df['INDUSTRY'].isin([20]),
            self.df['INDUSTRY'].isin([21]),
            self.df['INDUSTRY'].isin([22]),
            self.df['INDUSTRY'].isin([23]),
        ]

        values = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'E']
        self.df['ECONOMIC_SUB_SECTOR_CODE_ISIC'] = np.select(conditions, values, default='NA')
        return self

    def map_bank_relation(self):
        conditions = [
            self.df['BANK_RELATION'].isin(['NO RELATION']),
        ]

        values = ['NON']
        self.df['RELATED_PARTY'] = np.select(conditions, values, default='NA')
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
        self.df['OCCUPATION'] = self.df['OCCUPATION'].fillna('')
        
        self.df['OCCUPATION'] = np.where(
            self.df['OCCUPATION'].str.match(r'^\d+$') | (self.df['OCCUPATION'] == ''),
            99,
            self.df['OCCUPATION']
        )
        
        self.df['OCCUPATION'] = pd.to_numeric(self.df['OCCUPATION'], errors='coerce').fillna(99).astype(int)
        return self
    
    def get_mapped_dataframe(self):
        return self.df