import numpy as np
from datetime import datetime
import pandas as pd

class MappMoneyTransfer:
    def __init__(self, df):
        self.df = df

    def map_legal_doc_code(self):
        conditions = [
            self.df['TT_LEGAL_DOC'] == 'ASSOCIATION',
            self.df['TT_LEGAL_DOC'] == 'CEPGL.ID',
            self.df['TT_LEGAL_DOC'] == 'COMPANY',
            self.df['TT_LEGAL_DOC'] == 'COOPERATIVE',
            self.df['TT_LEGAL_DOC'] == 'EAC.ID',
            self.df['TT_LEGAL_DOC'] == 'EMBASSY',
            self.df['TT_LEGAL_DOC'] == 'FINANCIAL',
            self.df['TT_LEGAL_DOC'] == 'GUARDIAN',
            self.df['TT_LEGAL_DOC'] == 'IBIMINA',
            self.df['TT_LEGAL_DOC'] == 'NATIONAL.ID',
            self.df['TT_LEGAL_DOC'] == 'NATIONAL.ID.FOR',
            self.df['TT_LEGAL_DOC'] == 'NATIONAL.ID.REF',
            self.df['TT_LEGAL_DOC'] == 'NGO',
            self.df['TT_LEGAL_DOC'] == 'NPO',
            self.df['TT_LEGAL_DOC'] == 'PASSPORT',
            self.df['TT_LEGAL_DOC'] == 'PUBLIC',
            self.df['TT_LEGAL_DOC'] == 'CHILD.ID'
        ]
        
        values = ['9', '5', '6', '6', '5', '7', '6', '2', '9', '2', '5', '3', '6', '6', '4', '7', '8']
        
        self.df['ID_TYPE'] = np.select(conditions, values, default=np.nan)
        return self

    def map_remittence_type(self):
        conditions = [
            self.df['TRANSACTION_CODE'].isin(['35', '37']),
            self.df['TRANSACTION_CODE'].isin(['36', '38'])
        ]
        
        values = ['INW', 'OUW']
        
        self.df['REMITTANCE_TYPE'] = np.select(conditions, values, default=np.nan)
        return self

    def map_transaction_code(self):
        conditions = [
            self.df['TRANSACTION_CODE'].isin(['35', '36']),
            self.df['TRANSACTION_CODE'].isin(['37', '38'])
        ]
        
        values = ['WU', 'MG']
        
        self.df['MTO LIST'] = np.select(conditions, values, default=np.nan)
        return self

    def map_customer_name(self):
        self.df['CUSTOMER_NAME'] = np.where(
            self.df['TRANSACTION_CODE'].isin(['35', '37']),
            self.df['TT_RECIEVER'],
            self.df['NARRATIVE_2']
        )
        return self

    def map_other_id_type(self):
        conditions = [
            self.df['TT_OTHER_ID'] == 'ASSOCIATION',
            self.df['TT_OTHER_ID'] == 'CEPGL.ID',
            self.df['TT_OTHER_ID'] == 'COMPANY',
            self.df['TT_OTHER_ID'] == 'COOPERATIVE',
            self.df['TT_OTHER_ID'] == 'EAC.ID',
            self.df['TT_OTHER_ID'] == 'EMBASSY',
            self.df['TT_OTHER_ID'] == 'FINANCIAL',
            self.df['TT_OTHER_ID'] == 'GUARDIAN',
            self.df['TT_OTHER_ID'] == 'IBIMINA',
            self.df['TT_OTHER_ID'] == 'NATIONAL.ID',
            self.df['TT_OTHER_ID'] == 'NATIONAL.ID.FOR',
            self.df['TT_OTHER_ID'] == 'NATIONAL.ID.REF',
            self.df['TT_OTHER_ID'] == 'NGO',
            self.df['TT_OTHER_ID'] == 'NPO',
            self.df['TT_OTHER_ID'] == 'PASSPORT',
            self.df['TT_OTHER_ID'] == 'PUBLIC',
            self.df['TT_OTHER_ID'] == 'CHILD.ID'
        ]
        
        values = [9, 5, 6, 6, 5, 7, 6, 2, 9, 2, 5, 3, 6, 6, 4, 7, 8]
        
        self.df['OTHER_ID_TYPE'] = np.select(conditions, values, default=np.nan)
        return self

    def map_residents_flag(self):
        self.df['RESIDENTS_FLAG'] = np.where(self.df['RESIDENTS_FLAG'] == 'RW', 'R', 'NR')
        return self

    def get_mapped_dataframe(self):
        return self.df