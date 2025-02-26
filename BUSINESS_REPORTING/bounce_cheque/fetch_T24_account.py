import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
import pandas as pd
import time
from is_data_validation.FieldsAnalyzer import FieldsAnalyzer
from is_data_validation.db_connector import DBConnector
import os 
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

start_t = time.time()
st_time = datetime.now()

TEST_ITERATION = os.environ.get("TEST_ITERATION", None)

IS_POST_COB = os.environ.get("IS_POST_COB",None)
if str(IS_POST_COB).lower()=='true':
    IS_POST_COB = True
else:
    IS_POST_COB = False

oracle_query = """ 
SELECT 
    A.RECID AS ACCOUNT_NO,
    EXTRACTVALUE(A.XMLRECORD, '/row/c100[1]/text()') as ALT_ACC
FROM 
    T24.FBNK_ACCOUNT A
"""
# NOTES
    # seek info about the field of country being used

db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="OLD_ACCOUNT",
                       test_iter=TEST_ITERATION)
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
