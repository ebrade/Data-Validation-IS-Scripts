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
SELECT C.RECID, 
    C.COMPANY_CODE, 
    C.COMPANY_NAME AS OUC_DESCRIPTION, 
    C.VILLAGE_ID AS VILLAGE_LIST, 
    C.PROVINCE AS BRANCH_CATEGORY, 
    C.BR_OPEN_DATE AS BRANCH_OPEN_DATE, 
    C.BR_CLOSED_DATE AS BRANCH_CLOSE_DATE, 
    C.BR_STATUS AS BRANCH_STATUS, 
    C.BR_RURAL_URBAN AS SUB_BRANCH_FLAG,
    C.DATE_TIME AS DATE_LAST_MODIFIED,
    C.BR_LIC_DATE AS BRANCH_LICENSE_DATE,
    D.LAST_WORKING_DAY AS BUSINESS_DATE
    FROM T24.V_F_COMPANY C
   
    LEFT JOIN 
    T24.V_F_DATES D
    
    ON 
    C.RECID = D.COMPANY_CODE       
"""

# NOTES
    # seek info about the field of country being used

db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="BRANCH_INFO",
                       test_iter=TEST_ITERATION)
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
