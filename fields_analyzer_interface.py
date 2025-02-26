from abc import ABC, abstractmethod
import pandas as pd
import os


class FieldsAnalyzerInterface(ABC):
    @abstractmethod
    def check_accuracy(self):
        """Check accuracy of data"""
        pass
    
    @abstractmethod
    def load_destination_data(self):
        """Load destination data"""
        pass
    
    @abstractmethod
    def load_source_data(self):
        """Load source data"""
        pass

    def check_equality(self, row, col, destination, source):
        nuodb_col = f"{col}_{destination}"
        oracle_col = f"{col}_{source}"
        
        if row[nuodb_col] and row[oracle_col] and str(row[nuodb_col]).strip()==str(row[oracle_col]).strip():
            return True
        elif pd.isna(row[nuodb_col])  and pd.isna(row[oracle_col]):
            return True
        else:
            return False

    def check_row_exception(self, row, cols_to_check, destination, source):
        for col in cols_to_check:
            row_nam =  f"{col}_OK"           
            row[row_nam] = self.check_equality(row=row, col=col, destination=destination, source=source)
        return row
    
    def check_root_path(self, root_output_path):
        is_dir = os.path.isdir(root_output_path)
        if is_dir:
            pass
        else:
            os.makedirs(root_output_path)

    def construct_root(self, test_iteration, file_checked):
        root_path =  f"./EXCEPTIONS/{test_iteration}"
        self.check_root_path(root_path)
        return root_path

    def export_exceptions(self, df,  recid, cols_to_check, destination, source, test_iteration, file_checked):
        root_path = self.construct_root(test_iteration, file_checked)
        for col in cols_to_check: 
            if not df.empty:                     
                excep = df[df[f'{col}_OK']==False][[recid,f'{col}_{destination}',f'{col}_{source}']]
                if not excep.empty:
                    excep.to_csv(f"/BUSINESS_REPORTING/EXCEPTIONS/{root_path}/{col}_Exceptions.csv", index=False, sep="|")            
        print("Exporting Fields exceptions complete.............")
    
    def export_missing_data(self, destination_df, source_db, recid, destination, source, test_iteration, file_checked):
        root_path = self.construct_root(test_iteration, file_checked)
        NotInOracleDB = destination_df[~destination_df[recid].isin(source_db[recid])]
        if not NotInOracleDB.empty:
            NotInOracleDB.to_csv(f"{root_path}/NotIn{source}.csv", index=False, sep="|" )
        
        NotInNuoDB = source_db[~source_db[recid].isin(destination_df[recid])]
        if not NotInNuoDB.empty:
            NotInNuoDB.to_csv(f"{root_path}/NotIn{destination}.csv", index=False, sep="|" )

    def export_original_data(self, destination_df, oracle_df, file_checked, destination, source):
        root_path = self.construct_root()
        destination_df.to_csv(f"{root_path}/{file_checked}_{destination}_DATA_OG.csv", index=False, sep="|")
        oracle_df.to_csv(f"{root_path}/{file_checked}_{source}_DATA_OG.csv", index=False, sep="|")