import pandas as pd
import os
import re

class FieldsAnalyzer:
    def __init__(
        self, cols_to_check=None, file_checked=None, test_iter=None, is_post_cob=False
    ) -> None:
        self.cols_to_check = cols_to_check
        self.file_checked = file_checked
        self.test_iteration = test_iter
        self.cob_status = "POST_COB" if is_post_cob else "PRE_COB"

    
    def is_empty_or_na(self,val):
        if pd.isna(val):  # Handle NaN, None
            return True
        if isinstance(val, str):  # Handle strings
            return self.clean_col(val) == ""
        if isinstance(val, (list, tuple, dict, set)):  # Handle empty containers
            return len(val) == 0
        return False  # Default case
    @staticmethod
    def clean_col(val):
        return re.sub(r'\s+', '', str(val).replace("\x00", "").replace('"', '').replace('|', '').replace("-", ""))
    def check_equality(self, row, col):
        crm_col = f"{col}_PREMISE"
        oracle_col = f"{col}_CLOUD"
        x_crm = row.get(crm_col, None)
        x_oracle = row.get(oracle_col, None)
        if pd.notna(x_oracle) and x_oracle != '':
            x_oracle = x_oracle.zfill(len(str(x_crm)))

        

        # Both are NaN or empty
        if self.is_empty_or_na(x_crm) and self.is_empty_or_na(x_oracle):
            return True

        # One is empty/NaN, the other is NaN or empty
        if self.is_empty_or_na(x_crm) or self.is_empty_or_na(x_oracle):
            
            return self.clean_col(x_crm) == "" and pd.isna(x_oracle) or \
                   pd.isna(x_crm) and self.clean_col(x_oracle) == ""

        return self.clean_col(x_crm) == self.clean_col(x_oracle)
    def check_row_exception(self, row):
        for col in self.cols_to_check:
            row_nam = f"{col}_OK"
            row[row_nam] = self.check_equality(row=row, col=col)
            # print(row)
        return row

    def check_root_path(self, root_output_path):
        is_dir = os.path.isdir(root_output_path)
        if is_dir:
            pass
        else:
            os.makedirs(root_output_path)

    def construct_root(self):
        root_path = f"./{self.test_iteration}/"
        self.check_root_path(root_path)
        return root_path

    def export_exceptions(self, df, recid,file_date):
        root_path = self.construct_root()
        root_path = os.path.join(root_path, "CUSTOMER_PRODUCT_INFO",file_date)
        os.makedirs(root_path, exist_ok=True)
        for col in self.cols_to_check:
            if not df.empty:
                excep = df[df[f"{col}_OK"] == False][
                    [recid, f"{col}_PREMISE", f"{col}_CLOUD"]
                ]
                if not excep.empty:
                    excep.to_csv(
                        f"{root_path}/{col}_Exceptions.csv",
                        index=False,
                        sep="|",
                    )
        print("Exporting Fields exceptions complete.............")

    def export_missing_data(self, crm_df, oracle_db, recid,file_date):

            # crmdb_df=self.crmdb_data,
            # oracle_db=self.oracle_data,
            # recid="arrangement_customer",
    
        root_path = self.construct_root()
        root_path = os.path.join(root_path, "CUSTOMER_PRODUCT_INFO",file_date)
        os.makedirs(root_path, exist_ok=True)
        NotInOracleDB = crm_df[~crm_df[recid].isin(oracle_db[recid])]
        if not NotInOracleDB.empty:
            NotInOracleDB.to_csv(
                f"{root_path}/NotInCLOUD.csv",
                index=False,
                sep="~",
            )

        NotInCRMDB = oracle_db[~oracle_db[recid].isin(crm_df[recid])]
        if not NotInCRMDB.empty:
            NotInCRMDB.to_csv(
                f"{root_path}/NotInCRMDB.csv",
                index=False,
                sep="|",
            )

    # def export_original_data(self, crm_df, oracle_df):
    #     root_path = self.construct_root()
    #     crm_df.to_csv(
    #         f"{root_path}/{self.file_checked}_NuoDB_DATA_OG.csv", index=False, sep="|"
    #     )
    #     oracle_df.to_csv(
    #         f"{root_path}/{self.file_checked}_ORACLE_DATA_OG.csv", index=False, sep="|"
    #     )
