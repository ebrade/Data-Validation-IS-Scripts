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
SELECT RECID AS SEQUENCE_NUMBER,
    EXTRACTVALUE(XMLRECORD,'/row/c1[1]/text()') AS TRANSACTION_CODE,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=23]/text()') AS TT_RECIEVER,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=22]/text()') AS TT_LEGAL_DOC,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=19]/text()') AS Identification_Number,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=29]/text()') AS Other_party_name,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=31]/text()') AS Other_ID_Number,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=32]/text()') AS Remittance_Country,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=36]/text()') AS Transaction_Purpose,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=21]/text()') AS Residents_Flag,
    EXTRACTVALUE(XMLRECORD,'/row/c65[@m=30]/text()') AS TT_OTHER_ID,
    EXTRACTVALUE(XMLRECORD,'/row/c4[1]/text()') AS CURRENCY,
    EXTRACTVALUE(XMLRECORD,'/row/c20[1]/text()') AS Amount_Lcy,
    EXTRACTVALUE(XMLRECORD,'/row/c8[1]/text()') AS Amount_Fcy,
    EXTRACTVALUE(XMLRECORD,'/row/c37[1]/text()') AS Fees_And_Commission,
    EXTRACTVALUE(XMLRECORD,'/row/c11[1]/text()') AS Business_Date,
    EXTRACTVALUE(XMLRECORD,'/row/c28[1]/text()') AS NARRATIVE_2

FROM  T24.FBNK_TELLER#HIS WHERE EXTRACTVALUE(XMLRECORD,'/row/c1[1]/text()') IN ('35','36','37','38')
"""
db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="MONEY_TRANSFER",
                       test_iter=TEST_ITERATION)
print('Connected to DB.........................')
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
# root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA_OG.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
