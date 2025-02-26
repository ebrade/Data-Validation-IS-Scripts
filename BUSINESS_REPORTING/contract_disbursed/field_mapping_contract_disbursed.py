import numpy as np
from datetime import datetime
import pandas as pd

class ContractDisbursedMapping():
    def __init__(self, df):
        self.df = df

    def map_previous_disbursed_amt(self):        
        self.df['PREVIOUS_DISBURSED_AMT'] = self.df['PREVIOUS_DISBURSED_AMT'].fillna(0)
        return self
    
    def get_mapped_dataframe(self):
        return self.df