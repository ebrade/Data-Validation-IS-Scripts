import numpy as np
from datetime import datetime
import pandas as pd

class BranchInfoMapping():
    def __init__(self, df):
        self.df = df


    def map_branch_status(self):
        conditions = [
            self.df['BRANCH_STATUS'] == 'ACTIVE',
            self.df['BRANCH_STATUS'] == 'INACTIVE',
            self.df['BRANCH_STATUS'] == 'CLOSED'
        ]
       
        values = [0, 1, 9]
        self.df['BRANCH_STATUS'] = np.select(conditions, values)
        return self
    
    def map_sub_branch_flag(self):
        conditions = [
            self.df['VISION_OUC'] == '10001',
        ]
       
        values = [1]
        self.df['SUB_BRANCH_FLAG'] = np.select(conditions, values, default=2)
        return self
    
 

    def get_mapped_dataframe(self):
        return self.df