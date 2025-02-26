import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
import pandas as pd
from datetime import datetime
from is_data_validation.fields_analyzer_interface import FieldsAnalyzerInterface
from is_data_validation.df_generator import DFGenerator



class MoneyTransferAnalyzer(FieldsAnalyzerInterface):
    def __init__(self,  cols=None, 
                 file_checked=None, 
                 test_iter=None, 
                 source_name=None,
                 destination_name=None,
                 identifier=None) -> None:
        
        self.destination_data = None
        self.source_data = None
        self.merged_df = None

        self.cols_to_check = cols
        self.file_checked = file_checked
        self.test_iter = test_iter
        self.source_name = source_name
        self.destination_name=destination_name
        self.identifier = identifier
    
    def convert_date(self,date_string):
        if pd.isna(date_string):  
            return None  
        try:
            return datetime.strptime(date_string, "%Y%m%d").strftime("%d-%b-%Y")
        except ValueError:
            return None

    def load_destination_data(self):
        # f = f"{super().construct_root(self.test_iter, self.file_checked, self.is_post_cob)}/{self.file_checked}_{self.destination_name}_DATA_OG.csv"
        f = f"../Data/Destination/{self.file_checked}.csv"
        dfInstance = DFGenerator(filename=f, file_type = 'csv')
        self.destination_data = dfInstance.read_special_csv()

    def load_source_data(self):
        # f = f"{super().construct_root(self.test_iter, self.file_checked, self.is_post_cob)}/{self.file_checked}_{self.source_name}_DATA_OG.csv"
        f = f"../Data/Source/{self.file_checked}.csv"

        dfInstance = DFGenerator(filename=f, file_type = 'csv')
        self.source_data = dfInstance.read_special_csv()
        self.source_data.columns = self.source_data.columns.str.replace('_',' ')

    
    def check_accuracy(self):
        self.merged_df = pd.merge(self.destination_data, self.source_data, on=self.identifier, how='inner', indicator=True, suffixes=(f"_{self.destination_name}", f"_{self.source_name}"))
        dict_s = []
        for row in self.merged_df.to_dict(orient='records'):
            n_row = super().check_row_exception(row=row, cols_to_check=self.cols_to_check, destination=self.destination_name, source=self.source_name)           
            dict_s.append(n_row)
        self.merged_df = pd.DataFrame(dict_s)
        dict_s.clear()
    
    def export_exceptions(self):
        super().export_missing_data(
            destination_df=self.destination_data, 
            source_db=self.source_data,
            recid=self.identifier,
            destination=self.destination_name, 
            source=self.source_name,
            test_iteration=self.test_iter, 
            file_checked=self.file_checked, 
            )
        
        super().export_exceptions(
            df=self.merged_df, 
            recid=self.identifier,
            cols_to_check=self.cols_to_check, 
            destination=self.destination_name, 
            source=self.source_name,
            test_iteration=self.test_iter, 
            file_checked=self.file_checked, 
        )