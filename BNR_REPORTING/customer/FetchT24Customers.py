# import DFGenerator
import pandas as pd
import time
from FieldsAnalyzer import FieldsAnalyzer
from DBConnector import DBConnector
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
SELECT RECID as CUSTOMER_ID,
        EXTRACTVALUE(xmlrecord,'/row/c162[1]/text()') AS country,
        EXTRACTVALUE(xmlrecord,'/row/c3[1]/text()') AS forename_1,
        EXTRACTVALUE(xmlrecord,'/row/c4[1]/text()') AS forename_2,
        EXTRACTVALUE(xmlrecord,'/row/c61[1]/text()') AS surname,
        EXTRACTVALUE(xmlrecord,'/row/c61[1]/text()') AS customer_acronym,
        EXTRACTVALUE(xmlrecord,'/row/c60[1]/text()') AS salutation,
        EXTRACTVALUE(xmlrecord,'/row/c48[1]/text()') as Vision_OUC,
        EXTRACTVALUE(xmlrecord,'/row/c179[1]/text()') AS Sub_Seg,
        EXTRACTVALUE(xmlrecord,'/row/c24[1]/text()') AS Account_Officer,
        EXTRACTVALUE(xmlrecord,'/row/c100[1]/text()') AS Customer_Open_Date,
        EXTRACTVALUE(xmlrecord,'/row/c63[1]/text()') AS Gender,
        EXTRACTVALUE(xmlrecord,'/row/c183[1]/text()') AS inputter,
        EXTRACTVALUE(xmlrecord,'/row/c64[1]/text()') AS date_of_birth,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="162"][1]/text()' ) AS place_of_birth,
        EXTRACTVALUE(xmlrecord,'/row/c65[1]/text()') AS marital_status,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="40"][1]/text()') AS Spouse_Name,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="125"][1]/text()') AS Social_Economic_Class,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="28"][1]/text()') AS next_of_kin_name,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="32"][1]/text()') AS NEXTKIN_ID_TYPE_IN,    
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="31"][1]/text()') AS next_kin_id_number,    
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="29"][1]/text()') AS next_kin_tel,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="30"][1]/text()') AS next_kin_email,
        EXTRACTVALUE(xmlrecord,'/row/c66[1]/text()') AS number_of_dependants,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="127"][1]/text()') AS account_mandate_name,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="128"][1]/text()') AS account_mandate_id_type,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="129"][1]/text()') AS account_mandate_id_number,
        EXTRACTVALUE(xmlrecord,'/row/c28[1]/text()') AS nationality,
        EXTRACTVALUE(xmlrecord,'/row/c28[1]/text()') AS residence,
        EXTRACTVALUE(xmlrecord,'/row/c5[1]/text()') AS COMM_ADDRESS_1,
        EXTRACTVALUE(xmlrecord,'/row/c6[1]/text()') AS COMM_ADDRESS_2,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="19"][1]/text()') AS Comm_Village,
        EXTRACTVALUE(xmlrecord,'/row/c7[1]/text()') AS COMM_COUNTRY,
        EXTRACTVALUE(xmlrecord,'/row/c84[1]/text()') AS RESIDENCE_STATUS,
        EXTRACTVALUE(xmlrecord,'/row/c5[1]/text()') AS PERM_ADDRESS_1,
        EXTRACTVALUE(xmlrecord,'/row/c6[1]/text()') AS PERM_ADDRESS_2,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="19"][1]/text()') AS Perm_Village,
        EXTRACTVALUE(xmlrecord,'/row/c7[1]/text()') as PERM_COUNTRY,
        EXTRACTVALUE(xmlrecord,'/row/c69[1]/text()') as Email_ID,
        EXTRACTVALUE(xmlrecord,'/row/c68[1]/text()') as Home_Telephone,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="130"][1]/text()') as Bk_Education,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="95"][1]/text()') as Customer_TIN,
        EXTRACTVALUE(xmlrecord,'/row/c26[1]/text()') as Industry,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="23"][1]/text()') as BANK_RELATION,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="163"][1]/text()') as Related_Party_Name,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="132"][1]/text()') as Local_Govt_Member,
        EXTRACTVALUE(xmlrecord,'/row/c137[1]/text()') as INTERNET_BANKING_SERVICE,
        EXTRACTVALUE(xmlrecord,'/row/c138[1]/text()') as MOBILE_BANKING_SERVICE,
        EXTRACTVALUE(xmlrecord,'/row/c72[1]/text()') as occupation,
        EXTRACTVALUE(xmlrecord,'/row/c74[1]/text()') as employer_name,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="39"][1]/text()' ) as Employee_ID,
        EXTRACTVALUE(xmlrecord,'/row/c79[1]/text()' ) as Income,
        EXTRACTVALUE(xmlrecord,'/row/c81[1]/text()' ) as Income_Frequency,         
        EXTRACTVALUE(xmlrecord,'/row/c29[1]/text()' ) as Customer_Status,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="131"][1]/text()') as relationship_type,
        EXTRACTVALUE(xmlrecord,'/row/c35[1]/text()') as National_ID_Type,
        EXTRACTVALUE(xmlrecord,'/row/c34[1]/text()' ) as National_ID_Number,
        EXTRACTVALUE(xmlrecord,'/row/c54[1]/text()' ) as Group_Name,
        EXTRACTVALUE(xmlrecord,'/row/c53[1]/text()' ) as Group_Id,
        EXTRACTVALUE(xmlrecord,'/row/c184[1]/text()' ) as DATE_LAST_MODIFIED        
        
    FROM T24.FBNK_CUSTOMER
"""

# NOTES
    # seek info about the field of country being used

db_con = DBConnector(nuodb_query=None, oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="CUSTOMER",
                       test_iter=TEST_ITERATION)
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
root_folder = f_ins.construct_root()
oracle_data.to_csv(f"{root_folder}/DATA/{f_ins.file_checked}_ORACLE_DATA_OG.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
