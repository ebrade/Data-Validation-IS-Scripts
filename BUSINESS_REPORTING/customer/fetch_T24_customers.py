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
SELECT A.RECID as CUSTOMER_ID,
        EXTRACTVALUE(A.xmlrecord,'/row/c162[1]/text()') AS country,
        EXTRACTVALUE(A.xmlrecord,'/row/c3[1]/text()') AS forename_1,
        EXTRACTVALUE(A.xmlrecord,'/row/c4[1]/text()') AS forename_2,
        EXTRACTVALUE(A.xmlrecord,'/row/c2[1]/text()') AS SHORT_NAME,
        EXTRACTVALUE(A.xmlrecord,'/row/c62[1]/text()') AS surname,
        EXTRACTVALUE(A.xmlrecord,'/row/c61[1]/text()') AS customer_acronym,
        EXTRACTVALUE(A.xmlrecord,'/row/c60[1]/text()') AS salutation,
        EXTRACTVALUE(A.xmlrecord,'/row/c48[1]/text()') as COMPANY_BOOK,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[1]/text()') AS SEGMENT,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="164"]/text()') as SUB_SEG,
        EXTRACTVALUE(A.xmlrecord,'/row/c24[1]/text()') AS Account_Officer,
        EXTRACTVALUE(A.xmlrecord,'/row/c100[1]/text()') AS Customer_Open_Date,
        EXTRACTVALUE(A.xmlrecord,'/row/c63[1]/text()') AS Gender,
        EXTRACTVALUE(A.xmlrecord,'/row/c183[1]/text()') AS inputter,
        EXTRACTVALUE(A.xmlrecord,'/row/c64[1]/text()') AS date_of_birth,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="162"][1]/text()' ) AS place_of_birth,
        EXTRACTVALUE(A.xmlrecord,'/row/c65[1]/text()') AS marital_status,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="40"][1]/text()') AS Spouse_Name,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="125"][1]/text()') AS Social_Economic_Class,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="28"][1]/text()') AS next_of_kin_name,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="32"][1]/text()') AS NEXTKIN_ID_TYPE_IN,    
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="31"][1]/text()') AS next_kin_id_number,    
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="29"][1]/text()') AS next_kin_tel,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="30"][1]/text()') AS next_kin_email,
        EXTRACTVALUE(A.xmlrecord,'/row/c66[1]/text()') AS number_of_dependants,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="127"][1]/text()') AS account_mandate_name,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="128"][1]/text()') AS account_mandate_id_type,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="129"][1]/text()') AS account_mandate_id_number,
        EXTRACTVALUE(A.xmlrecord,'/row/c28[1]/text()') AS nationality,
        EXTRACTVALUE(A.xmlrecord,'/row/c28[1]/text()') AS residence,
        EXTRACTVALUE(A.xmlrecord,'/row/c5[1]/text()') AS COMM_ADDRESS_1,
        EXTRACTVALUE(A.xmlrecord,'/row/c6[1]/text()') AS COMM_ADDRESS_2,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="19"][1]/text()') AS Comm_Village,
        EXTRACTVALUE(A.xmlrecord,'/row/c162[1]/text()') AS COMM_COUNTRY,
        EXTRACTVALUE(A.xmlrecord,'/row/c84[1]/text()') AS RESIDENCE_STATUS,
        EXTRACTVALUE(A.xmlrecord,'/row/c5[1]/text()') AS PERM_ADDRESS_1,
        EXTRACTVALUE(A.xmlrecord,'/row/c6[1]/text()') AS PERM_ADDRESS_2,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="18"][1]/text()') AS Village_ID,
        EXTRACTVALUE(A.xmlrecord,'/row/c162[1]/text()') as PERM_COUNTRY,
        EXTRACTVALUE(A.xmlrecord,'/row/c69[1]/text()') as Email_ID,
        EXTRACTVALUE(A.xmlrecord,'/row/c68[1]/text()') as Home_Telephone,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="130"][1]/text()') as Bk_Education,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="95"][1]/text()') as Customer_TIN,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m=142]/text()') AS ALT_CUSTOMER,
        EXTRACTVALUE(A.xmlrecord,'/row/c26[1]/text()') as Industry,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="23"][1]/text()') as BANK_RELATION,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="163"][1]/text()') as Related_Party_Name,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="132"][1]/text()') as Local_Govt_Member,
        EXTRACTVALUE(A.xmlrecord,'/row/c137[1]/text()') as INTERNET_BANKING_SERVICE,
        EXTRACTVALUE(A.xmlrecord,'/row/c138[1]/text()') as MOBILE_BANKING_SERVICE,
        EXTRACTVALUE(A.xmlrecord,'/row/c72[1]/text()') as occupation,
        EXTRACTVALUE(A.xmlrecord, '/row/c23[1]/text()') as Sector,
        EXTRACTVALUE(A.xmlrecord, '/row/c42[1]/text()') as BIRTH_INCORP_DATE,
        EXTRACTVALUE(A.xmlrecord, '/row/c38[1]/text()') as LEGAL_ISS_DATE,
        EXTRACTVALUE(A.xmlrecord,'/row/c74[1]/text()') as employer_name,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="39"][1]/text()' ) as Employee_ID,
        EXTRACTVALUE(A.xmlrecord,'/row/c79[1]/text()' ) as Income,
        EXTRACTVALUE(A.xmlrecord,'/row/c81[1]/text()' ) as Income_Frequency,         
        EXTRACTVALUE(A.xmlrecord,'/row/c29[1]/text()' ) as Customer_Status,
        EXTRACTVALUE(A.xmlrecord,'/row/c179[@m="131"][1]/text()') as relationship_type,
        EXTRACTVALUE(A.xmlrecord,'/row/c35[1]/text()') as LEGAL_DOC_NAME,
        EXTRACTVALUE(A.xmlrecord,'/row/c34[1]/text()' ) as National_ID_Number,
        EXTRACTVALUE(A.xmlrecord,'/row/c54[1]/text()' ) as Group_Name,
        EXTRACTVALUE(A.xmlrecord,'/row/c53[1]/text()' ) as Group_Id,
        EXTRACTVALUE(A.xmlrecord,'/row/c184[1]/text()' ) as DATE_LAST_MODIFIED        
        
    FROM T24.FBNK_CUSTOMER A
"""

# NOTES
    # seek info about the field of country being used

db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="CUSTOMER",
                       test_iter=TEST_ITERATION)
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
