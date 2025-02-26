import numpy as np
from datetime import datetime
import pandas as pd

class ContractScheduleMapping():
    def __init__(self, df):
        self.df = df


    
    def get_mapped_dataframe(self):
        return self.df