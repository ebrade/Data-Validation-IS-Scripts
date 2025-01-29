import numpy as np
from datetime import datetime
import pandas as pd

class MappAccount:
    def __init__(self, df):
        self.df = df

    def map_credit_category(self):
        self.df['CATEGORY'] = pd.to_numeric(self.df['CATEGORY'], errors='coerce')
        conditions = [
            self.df['CATEGORY'].isin([1031, 3106, 3107, 3108, 3120, 3121, 3122, 3123]),
            self.df['CATEGORY'].isin([3018, 3019, 3054, 3055, 3092, 3094, 3096, 3097, 3099, 3104, 3148]),
            self.df['CATEGORY'].isin([3045, 3090, 3091, 3092, 3093]),
            self.df['CATEGORY'].isin([3053, 3095]),
            self.df['CATEGORY'].isin([3101]),
            self.df['CATEGORY'].isin([3098, 3105]),
            self.df['CATEGORY'].isin([3001, 3002, 3003, 3004, 3005, 3014, 3015, 3016, 3020, 3021, 3022, 3023, 3024]),
            self.df['CATEGORY'].isin([3006, 3007, 3009, 3025, 3026, 3027, 3109]),
            self.df['CATEGORY'].isin([3008, 3010, 3011, 3012, 3028, 3029, 3070, 3071, 3072, 3073, 3074, 3110]),
            self.df['CATEGORY'].isin([3030, 3031, 3032, 3040, 3041, 3042]),
            self.df['CATEGORY'].isin([3060]),
            self.df['CATEGORY'].isin([3017, 3033, 3034, 3035, 3036, 3037, 3038, 3039, 3043, 3044, 3045, 3046, 3047, 3048, 3049, 3050, 3051, 3052, 3080, 3081]),
            self.df['CATEGORY'].isin([3100, 3102, 3103]),
            (self.df['CATEGORY'] >= 23001) & (self.df['CATEGORY'] <= 23160),
            (self.df['CATEGORY'] >= 28000) & (self.df['CATEGORY'] <= 28199),
            self.df['CATEGORY'].isin([3013, 3199]),
        ]
        values = [10, 11, 20, 21, 22, 34, 40, 50, 60, 64, 68, 71, 72, 80, 83, 15]
        self.df['CREDIT_CATEGORY'] = np.select(conditions, values, default=89)
        return self
        
    def map_performance_class(self):
        conditions = [
            self.df['ARR_AGE_STATUS'] == 'LOS',
            self.df['ARR_AGE_STATUS'] == 'WAT',
            self.df['ARR_AGE_STATUS'].isin(['DOU', 'DEL']),
            self.df['ARR_AGE_STATUS'] == 'SUB',
            self.df['ARR_AGE_STATUS'] == 'WOF',
        ]
        values = ['LL', 'WL', 'DL', 'SL', 'WO']
        self.df['PERFORMANCE_CLASS'] = np.select(conditions, values, default='NL')
        return self
    
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
            self.df['SEGMENT'] == 1
        ]
        
        values = [
            'NGO', 'SAGRP', 'OTHER', 'RETL', 
            'LRGOTHR', 'MCEOTHR', 'MEDOTHR', 'SMLOTHR', 'LRGOTHR', 'RETL'
        ]
        self.df['VISION_SBU'] = np.select(conditions
            ,values, default=None)
        return self
    
    def map_account_status(self):
        # Convert dates from string format YYYYMMDD to datetime
        self.df['DATE_LAST_CR_CUST'] = pd.to_datetime(self.df['DATE_LAST_CR_CUST'], format='%Y%m%d', errors='coerce')
        self.df['DATE_LAST_DR_CUST'] = pd.to_datetime(self.df['DATE_LAST_DR_CUST'], format='%Y%m%d', errors='coerce')
        self.df['OPENING_DATE'] = pd.to_datetime(self.df['OPENING_DATE'], format='%Y%m%d', errors='coerce')

        # Define business date
        COB_DATE = datetime.strptime("2025-01-22", '%Y-%m-%d')

        # Calculate the most recent transaction date
        self.df['MOST_RECENT_DATE'] = self.df[['DATE_LAST_CR_CUST', 'DATE_LAST_DR_CUST']].max(axis=1)
        self.df['REFERENCE_DATE'] = self.df['MOST_RECENT_DATE'].combine_first(self.df['OPENING_DATE'])

        # Calculate months since the last transaction
        self.df['MONTHS_DIFF'] = (COB_DATE - self.df['REFERENCE_DATE']).dt.days / 30

        # Convert CATEGORY to numeric, coercing non-numeric values to NaN
        self.df['CATEGORY'] = pd.to_numeric(self.df['CATEGORY'], errors='coerce')

        # Define conditions
        conditions = [
            self.df['MONTHS_DIFF'] < 6,
            self.df['MONTHS_DIFF'].between(6, 12, inclusive='both'),
            ((self.df['CATEGORY'].between(0, 1999)) | 
            (self.df['CATEGORY'].between(2000, 2999)) | 
            (self.df['CATEGORY'].between(21000, 21030))) & (self.df['MONTHS_DIFF'] > 12)
        ]

        # Define values
        values = ['0', '1', '3']

        # Apply conditions
        self.df['ACCOUNT_STATUS'] = np.select(conditions, values, default='2')

        return self
    
    
    def map_account_type(self):
        
        self.df['CATEGORY'] = pd.to_numeric(self.df['CATEGORY'], errors='coerce')
        conditions=[
            self.df['CATEGORY'].between(0, 2999),                     # 'CAA'
            self.df['CATEGORY'].between(21000, 21030),                # 'CAA'
            self.df['CATEGORY'].between(20000, 20999),                # 'OAB'
            self.df['CATEGORY'] == 6701,                              # 'OAB'
            self.df['CATEGORY'] == 28000,                             # 'OAB'
            self.df['CATEGORY'].between(21031, 21999),                # 'OAB'
            self.df['CATEGORY'] == 23005,                             # 'LAA'
            self.df['CATEGORY'].between(3000, 3999),                  # 'LAA'
            self.df['CATEGORY'].between(4000, 4999),                  # 'LAA'
            self.df['CATEGORY'].between(23000, 23999),                # 'LAA'
            self.df['CATEGORY'].between(6600, 6999),                  # 'TDA'
            self.df['CATEGORY'].between(6000, 6599)                   # 'SBA'
        ]
        
        values = [
            'CAA',  # 0-2999
            'CAA',  # 21000-21030
            'OAB',  # 20000-20999
            'OAB',  # 6701
            'OAB',  # 28000
            'OAB',  # 21031-21999
            'LAA',  # 23005
            'LAA',  # 3000-3999
            'LAA',  # 4000-4999
            'LAA',  # 23000-23999
            'TDA',  # 6600-6999
            'SBA'   # 6000-6599
        ]
        # Apply conditions to create ACCOUNT_TYPE column
        self.df['ACCOUNT_TYPE'] = np.select(conditions, values, default=None)
        
        return self
        
    def map_freeze_status(self):
        
        conditions = [
            self.df['POSTING_RESTRICT'] == '1',       
            self.df['POSTING_RESTRICT'].isin(['2', '3', '5', '6', '7', '8', '9', '10', '11', '12', '13', '15', '16', '17', '18', '21', '22', '23', '24', '26', '50']),  # 'D'
            self.df['POSTING_RESTRICT'].isin(['4', '14', '19']),  
            self.df['POSTING_RESTRICT'].isin(['20', '60']),       
            self.df['POSTING_RESTRICT'].isin(['25', '31', '70', '80', '90']),  
        ]
        
        values = [
            'Y',  
            'D',  
            'Y',  
            'C',  
            'N',  
        ]
        
        self.df['FREEZE_STATUS'] = np.select(conditions, values, default='N')
        
        return self

    def map_public_sector_code(self):
        
        conditions = [
            self.df['SECTOR'].isin(['1000', '1001', '1002', '1003', '1004', '1005',
                               '2000', '2001',
                               '3000', '3001', '3002', '3003', '3004', '3005', '3006', '3007', '3008', '3009', '3010',
                               '4000', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009']),
            self.df['SECTOR'] == '5000',
            self.df['SECTOR'] == '5001',
            self.df['SECTOR'] == '5002',
            self.df['SECTOR'] == '5003',
            self.df['SECTOR'] == '5004',
            self.df['SECTOR'] == '5005',
            self.df['SECTOR'] == '5006',
            self.df['SECTOR'] == '5007',
            self.df['SECTOR'] == '5008',
            self.df['SECTOR'] == '5009',
            self.df['SECTOR'] == '5010',
            self.df['SECTOR'].isin(['5011']),
            self.df['SECTOR'] == '6000',
            self.df['SECTOR'] == '6001',
            self.df['SECTOR'] == '6002',
            self.df['SECTOR'] == '7000',
            self.df['SECTOR'] == '7001',
            self.df['SECTOR'] == '8000',
            self.df['SECTOR'] == '8001',
        ]
        
        values = [
            'O1',  # 
            'A1',  # 5000
            'A1',  # 5001
            'A2',  # 5002
            'A3',  # 5003
            'A4',  # 5004
            'A5',  # 5005
            'A6',  # 5006
            'A71',  # 5007
            'A72',  # 5008
            'A73',  # 5009
            'A74',  # 5010
            'A74',  # 5011
            'B1',  # 6000
            'B2',  # 6001
            'B3',  # 6002
            'C1',  # 7000
            'C2',  # 7001
            'D1',  # 8000
            'D2',  # 8001
        ]
        self.df['PUBLIC_SECTOR_CODE'] = np.select(conditions, values, default='O1')
        
        return self
        
    def map_institutional_sector_code(self):
        conditions = [
            self.df['SECTOR'] == '1000',  # INDIV
            self.df['SECTOR'] == '1001',  # NPMO
            self.df['SECTOR'] == '1002',  # MENT
            self.df['SECTOR'] == '1003',  # SENT
            self.df['SECTOR'] == '1004',  # SAVG
            self.df['SECTOR'] == '1005',  # NSAVG
            self.df['SECTOR'] == '2000',  # NFCPVT
            self.df['SECTOR'] == '2001',  # OLENT
            self.df['SECTOR'] == '3000',  # PSBA
            self.df['SECTOR'] == '3001',  # MLDB
            self.df['SECTOR'] == '3002',  # COMBNK
            self.df['SECTOR'] == '3003',  # INVB
            self.df['SECTOR'] == '3004',  # DEVB
            self.df['SECTOR'] == '3005',  # MFB
            self.df['SECTOR'] == '3006',  # COOPB
            self.df['SECTOR'] == '3007',  # ISLB
            self.df['SECTOR'] == '3008',  # BHRA
            self.df['SECTOR'] == '3009',  # MFI
            self.df['SECTOR'] == '3010',  # COMBNK
            self.df['SECTOR'] == '4000',  # INS
            self.df['SECTOR'] == '4001',  # SEC
            self.df['SECTOR'] == '4002',  # BROK
            self.df['SECTOR'] == '4003',  # PEN
            self.df['SECTOR'] == '4004',  # MFT
            self.df['SECTOR'] == '4005',  # MFIND
            self.df['SECTOR'] == '4006',  # CDHA
            self.df['SECTOR'] == '4007',  # FXB
            self.df['SECTOR'] == '4008',  # NMMIF
            self.df['SECTOR'] == '4009',  # OFIOTH
            self.df['SECTOR'] == '5000',  # CENBNK
            self.df['SECTOR'].isin(['5001', '5002', '5003', '5004', '5005', '5006', '5007', '5008', '5009']),  # CENGOV
            self.df['SECTOR'] == '5010',  # CENGOVF
            self.df['SECTOR'] == '5011',  # CENGOV
            self.df['SECTOR'].isin(['6000', '6001', '6002']),  # LOCGOV
            self.df['SECTOR'].isin(['7000', '7001']),  # PFGOV
            self.df['SECTOR'].isin(['8000', '8001'])   # NFCPUB
        ]
        
        values = [
            'INDIV', 'NPMO', 'MENT', 'SENT', 'SAVG', 'NSAVG', 'NFCPVT', 'OLENT',
            'PSBA', 'MLDB', 'COMBNK', 'INVB', 'DEVB', 'MFB', 'COOPB', 'ISLB', 'BHRA', 'MFI', 'COMBNK',
            'INS', 'SEC', 'BROK', 'PEN', 'MFT', 'MFIND', 'CDHA', 'FXB', 'NMMIF', 'OFIOTH',
            'CENBNK', 'CENGOV', 'CENGOVF', 'CENGOV', 'LOCGOV', 'PFGOV', 'NFCPUB'
        ]
        # Apply conditions to create INSTITUTIONAL_SECTOR_CODE column
        self.df['INSTITUTIONAL_SECTOR_CODE'] = np.select(conditions, values, default=None)
        
        return self

    def get_mapped_dataframe(self):
        return self.df