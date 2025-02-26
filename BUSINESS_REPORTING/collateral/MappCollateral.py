import numpy as np
from datetime import datetime
import pandas as pd

class MappCollateral:
    def __init__(self, df):
        self.df = df

    def map_collateral_type(self):
        # Define conditions and corresponding values
        conditions = [
            self.df['COLLATERAL_TYPE'] == '101',
            self.df['COLLATERAL_TYPE'] == '102',
            self.df['COLLATERAL_TYPE'] == '103',
            self.df['COLLATERAL_TYPE'] == '104',
            self.df['COLLATERAL_TYPE'] == '105',
            self.df['COLLATERAL_TYPE'] == '106',
            self.df['COLLATERAL_TYPE'] == '201',
            self.df['COLLATERAL_TYPE'] == '202',
            self.df['COLLATERAL_TYPE'] == '203',
            self.df['COLLATERAL_TYPE'] == '204',
            self.df['COLLATERAL_TYPE'] == '205',
            self.df['COLLATERAL_TYPE'] == '206',
            self.df['COLLATERAL_TYPE'] == '207',
            self.df['COLLATERAL_TYPE'] == '208',
            self.df['COLLATERAL_TYPE'] == '209',
            self.df['COLLATERAL_TYPE'] == '210',
            self.df['COLLATERAL_TYPE'] == '211',
            self.df['COLLATERAL_TYPE'] == '212',
            self.df['COLLATERAL_TYPE'] == '213',
            self.df['COLLATERAL_TYPE'] == '214',
            self.df['COLLATERAL_TYPE'] == '215',
            self.df['COLLATERAL_TYPE'] == '216',
            self.df['COLLATERAL_TYPE'] == '217',
            self.df['COLLATERAL_TYPE'] == '302',
            self.df['COLLATERAL_TYPE'] == '303',
            self.df['COLLATERAL_TYPE'] == '304',
            self.df['COLLATERAL_TYPE'] == '401',
            self.df['COLLATERAL_TYPE'] == '402',
            self.df['COLLATERAL_TYPE'] == '403',
            self.df['COLLATERAL_TYPE'] == '404',
            self.df['COLLATERAL_TYPE'] == '405',
            self.df['COLLATERAL_TYPE'] == '406',
            self.df['COLLATERAL_TYPE'] == '407',
            self.df['COLLATERAL_TYPE'] == '408',
            self.df['COLLATERAL_TYPE'] == '501',
            self.df['COLLATERAL_TYPE'] == '502',
            self.df['COLLATERAL_TYPE'] == '503',
            self.df['COLLATERAL_TYPE'] == '504',
            self.df['COLLATERAL_TYPE'] == '601',
            self.df['COLLATERAL_TYPE'] == '602',
            self.df['COLLATERAL_TYPE'] == '603',
            self.df['COLLATERAL_TYPE'] == '604',
            self.df['COLLATERAL_TYPE'] == '605',
            self.df['COLLATERAL_TYPE'] == '606',
            self.df['COLLATERAL_TYPE'] == '305',
            self.df['COLLATERAL_TYPE'] == '307',
            self.df['COLLATERAL_TYPE'] == '306',
            self.df['COLLATERAL_TYPE'] == '308',
            self.df['COLLATERAL_TYPE'] == '309',
            self.df['COLLATERAL_TYPE'] == '409'
        ]

        values = [
            'CA1', 'CA2', 'CA3', 'CA4', 'CA5', 'CA6',
            'FG1', 'FG2', 'FG3', 'FG4', 'FG5', 'FG6', 'FG7', 'FG8', 'FG9', 'FG10',
            'FG11', 'FG12', 'FG13', 'FG14', 'FG15', 'FG16', 'FG17',
            'IMA1', 'IMA2', 'IMA3',
            'MA1', 'MA2', 'MA3', 'MA4', 'MA5', 'MA6', 'MA7', 'MA8',
            'IIA1', 'IIA2', 'IIA3', 'IIA4',
            'OA1', 'OA2', 'OA3', 'OA4', 'OA5', 'OA6','IMA3','IMA2','IMA1','IMA3','IMA3','IMA1'
        ]

        self.df['COLLATERAL_TYPE'] = np.select(conditions, values, default='')

        return self
    
    def map_insured_status(self):
        self.df['INSURED'] = np.where(
            (self.df['INSURED_AMT'] == 'N') | (self.df['INSURED_AMT'].isna()), 
            'N', 
            'Y'
        )
        return self

    def map_ownership_status(self):
        self.df['COLLATERAL_OWNERSHIP'] = np.where(
            self.df['COLLATERAL_OWNERSHIP'].isna(), 
            '', 
            'Y'
        )
        return self

    def get_mapped_dataframe(self):
        return self.df