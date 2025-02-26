import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.df_generator import DFGenerator
import pandas as pd
import time
from is_data_validation.FieldsAnalyzer import FieldsAnalyzer
from is_data_validation.db_connector import DBConnector
import os 
from datetime import datetime
from dotenv import load_dotenv
import os
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
SELECT RECID as CUSTOMER_ID,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m=142]/text()') AS ALT_CUSTOMER
        
FROM T24.FBNK_CUSTOMER
"""
db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="ALT_CUSTOMER_ID",
                       test_iter=TEST_ITERATION)
print('Connected to DB.........................')
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
# root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA_OG.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
