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
SELECT 
    A.RECID AS Account_No,
    EXTRACTVALUE(A.XMLRECORD, '/row/c100[1]/text()') as ALT_ACC,
    EXTRACTVALUE(A.XMLRECORD, '/row/c8[1]/text()') as CURRENCY,
    EXTRACTVALUE(A.XMLRECORD, '/row/c5[1]/text()') as Account_Name,
    EXTRACTVALUE(A.XMLRECORD, '/row/c252[1]/text()') as Vision_OUC,
    EXTRACTVALUE(A.XMLRECORD, '/row/c71[1]/text()') as Account_Status,
    EXTRACTVALUE(B.XMLRECORD,'/row/c7[1]/text()' ) as ARR_AGE_STATUS,
    EXTRACTVALUE(B.XMLRECORD, '/row/c8[1]/text()') as Account_Status_date,
    EXTRACTVALUE(A.XMLRECORD, '/row/c1[1]/text()') as Customer_Id,
    EXTRACTVALUE(A.XMLRECORD, '/row/c11[1]/text()') as Account_Officer,
    EXTRACTVALUE(A.XMLRECORD, '/row/c8[1]/text()') as Currency,
    EXTRACTVALUE(A.XMLRECORD, '/row/c1[1]/text()') as Account_Type,
    EXTRACTVALUE(A.XMLRECORD, '/row/c78[1]/text()') as OPENING_DATE,
    EXTRACTVALUE(A.XMLRECORD, '/row/c90[1]/text()') as Account_Closing_Date,
    EXTRACTVALUE(A.XMLRECORD, '/row/c13[1]/text()') as POSTING_RESTRICT,
    EXTRACTVALUE(A.XMLRECORD, '/row/c34[1]/text()') as DATE_LAST_CR_CUST,
    EXTRACTVALUE(A.XMLRECORD, '/row/c37[1]/text()') as DATE_LAST_DR_CUST,
    EXTRACTVALUE(A.XMLRECORD, '/row/c105[1]/text()') as Joint_Participant_Count,
    EXTRACTVALUE(A.XMLRECORD, '/row/c2[1]/text()') as Category,
    EXTRACTVALUE(A.XMLRECORD, '/row/c167[1]/text()') as Date_Last_Modified ,
    EXTRACTVALUE(A.XMLRECORD,'/row/c45[1]/text()' ) as TRAN_LAST_DR_BANK,
    EXTRACTVALUE(A.XMLRECORD,'/row/c36[1]/text()' ) as TRAN_LAST_CR_BANK,
    EXTRACTVALUE(D.xmlrecord,'/row/c179[@m="164"]/text()') as SUB_SEG,
    EXTRACTVALUE(D.xmlrecord,'/row/c179[@m="146"][1]/text()' ) as Economic_Sector_Code,
    EXTRACTVALUE(D.xmlrecord,'/row/c179[@m="165"][1]/text()' ) as Economic_Sub_Sector_Code,
    EXTRACTVALUE(D.xmlrecord,'/row/c179[@m="165"][1]/text()' ) as ECONOMIC_SUB_SECTOR_CODE_ISIC,
    EXTRACTVALUE(D.XMLRECORD, '/row/c23[1]/text()') as Sector,
    EXTRACTVALUE(D.xmlrecord,'/row/c26[1]/text()' ) as INDUSTRY,
    EXTRACTVALUE(D.xmlrecord,'/row/c179[1]/text()') as SEGMENT,
    EXTRACTVALUE(D.XMLRECORD,'/row/c35[1]/text()' ) as LEGAL_DOC_NAME
    
FROM 
    T24.FBNK_ACCOUNT A
LEFT JOIN 
    T24.FBNK_AA_ACCOUNT_DET001 B 
ON 
    EXTRACTVALUE(A.XMLRECORD, '/row/c181[1]/text()') = B.RECID

LEFT JOIN 
    T24.F_CATEGORY  C
ON 
    EXTRACTVALUE(A.XMLRECORD, '/row/c2[1]/text()') = C.RECID   

LEFT JOIN 
    T24.FBNK_CUSTOMER  D
ON 
    EXTRACTVALUE(A.XMLRECORD, '/row/c1[1]/text()') = D.RECID
"""
db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="ACCOUNT",
                       test_iter=TEST_ITERATION)
print('Connected to DB.........................')
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
# root_folder = f_ins.construct_root()
oracle_data.to_csv(f"./Data/Source/{f_ins.file_checked}_ORACLE_DATA_OG.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
