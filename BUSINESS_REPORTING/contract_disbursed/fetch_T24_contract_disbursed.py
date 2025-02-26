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
SELECT RECID,
    EXTRACTVALUE(xmlrecord,'/row/c1[1]/text()') AS CONTRACT_ID,
    EXTRACTVALUE(xmlrecord,'/row/c7[1]/text()') AS CURRENCY,
    EXTRACTVALUE(xmlrecord,'/row/c42[1]/text()') AS CURRENT_DISBURSED_AMT,
    EXTRACTVALUE(xmlrecord, '/row/c42[@m="1" and @s="2"]/text()') AS PREVIOUS_DISBURSED_AMT
FROM T24.FBNK_AA_BILL_DETAILS
WHERE EXTRACTVALUE(xmlrecord,'/row/c72[1]/text()') = 'DISBURSEMENT'
"""

# SELECT RECID,
#         EXTRACTVALUE(xmlrecord,'/row/c3[1]/text()') AS BUSINESS_DATE,
#         EXTRACTVALUE(xmlrecord,'/row/c1[1]/text()') AS CONTRACT_ID,
#         EXTRACTVALUE(xmlrecord,'/row/c12[1]/text()') AS CURRENCY,
#         EXTRACTVALUE(xmlrecord,'/row/c47[1]/text()') AS TXN_AMOUNT_LCY,
#         EXTRACTVALUE(xmlrecord,'/row/c48[1]/text()') AS TXN_AMOUNT_LCY_2
#     FROM T24.FBNK_AA_ARRANGEMENT006



db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="CONTRACT_DISBURSED",
                       test_iter=TEST_ITERATION)
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
