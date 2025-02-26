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
    EXTRACTVALUE(xmlrecord,'/row/c1[1]/text()') AS YEAR_MONTH,
    EXTRACTVALUE(xmlrecord,'/row/c2[1]/text()') AS CONTRACT_ID,
    EXTRACTVALUE(xmlrecord,'/row/c3[1]/text()') AS SCHEDULE_DATE,
    EXTRACTVALUE(xmlrecord,'/row/c4[1]/text()') AS PAYMENT_DATE,
    EXTRACTVALUE(xmlrecord,'/row/c5[1]/text()') AS PRINCIPAL_AMOUNT_DUE_LCY,
    EXTRACTVALUE(xmlrecord,'/row/c6[1]/text()') AS PRINCIPAL_AMOUNT_DUE_FCY,
    EXTRACTVALUE(xmlrecord,'/row/c7[1]/text()') AS INT_AMOUNT_DUE_LCY,
    EXTRACTVALUE(xmlrecord,'/row/c8[1]/text()') AS INT_AMOUNT_DUE_FCY,
    EXTRACTVALUE(xmlrecord,'/row/c9[1]/text()') AS PRINCIPAL_AMOUNT_PAID_LCY,
    EXTRACTVALUE(xmlrecord,'/row/c10[1]/text()') AS PRINCIPAL_AMOUNT_PAID_FCY,
    EXTRACTVALUE(xmlrecord,'/row/c11[1]/text()') AS INT_AMOUNT_PAID_LCY,
    EXTRACTVALUE(xmlrecord,'/row/c12[1]/text()') AS INT_AMOUNT_PAID_FCY,
    EXTRACTVALUE(xmlrecord,'/row/c13[1]/text()') AS OUTSTANDING_AMOUNT_LCY,
    EXTRACTVALUE(xmlrecord,'/row/c14[1]/text()') AS OUTSTANDING_AMOUNT_FCY
FROM T24.FBNK_BOK_CONTRACT_S000
"""


db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="CONTRACT_SCHEDULE",
                       test_iter=TEST_ITERATION)
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")



