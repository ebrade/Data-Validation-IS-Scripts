import DFGenerator
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
SELECT RECID,
        EXTRACTVALUE(xmlrecord,'/row/c162/text()' ) as address_country,
        EXTRACTVALUE(xmlrecord, '/row/c45[1]/text()') AS language_1,
        EXTRACTVALUE(xmlrecord, '/row/c179[1]/text()') AS language_2,
        EXTRACTVALUE(xmlrecord, '/row/c104[1]/text()') AS language_3,
        EXTRACTVALUE(xmlrecord, '/row/c105[1]/text()') AS language_4,
        EXTRACTVALUE(xmlrecord, '/row/c60[1]/text()') AS title,
        EXTRACTVALUE(xmlrecord, '/row/c3[1]/text()') AS names,
        EXTRACTVALUE(xmlrecord, '/row/c4[1]/text()') AS given_name,
        EXTRACTVALUE(xmlrecord, '/row/c2[1]/text()') AS arrangement_customer_full_name,
        EXTRACTVALUE(xmlrecord, '/row/c63/text()' ) as gender,
        EXTRACTVALUE(xmlrecord,'/row/c64/text()' ) as dateofbirth,
        EXTRACTVALUE(xmlrecord,'/row/c42/text()' ) as dateofincorporation,
        EXTRACTVALUE(xmlrecord,'/row/c34[1]/text()' ) as legalid	,
        EXTRACTVALUE(xmlrecord,'/row/c38[1]/text()' ) as dateofissuesofidentityrecord,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="16"][1]/text()' ) as identityrecordplaceofissues,
        EXTRACTVALUE(xmlrecord,'/row/c65/text()' ) as maritalstatus,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="40"][1]/text()' ) as spousename,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="24"][1]/text()' ) as maritalagreement,
        EXTRACTVALUE(xmlrecord,'/row/c29/text()' ) as arrangement_customer_status,
        EXTRACTVALUE(xmlrecord,'/row/c27/text()' ) as customertarget,
        EXTRACTVALUE(xmlrecord,'/row/c6/text()' ) as customeraddress,
        EXTRACTVALUE(xmlrecord,'/row/c179[1]/text()') as SEGMENT,
        EXTRACTVALUE(xmlrecord,'/row/c23/text()' ) as SECTOR,
        EXTRACTVALUE(xmlrecord,'/row/c26/text()' ) as industry,
        EXTRACTVALUE(xmlrecord,'row/c100/text()' ) as openingdate,
        EXTRACTVALUE(xmlrecord,'/row/c69[1]/text()' ) as email,
        EXTRACTVALUE(xmlrecord,'/row/c68[1]/text()' ) as phoneno,
        EXTRACTVALUE(xmlrecord,'/row/c48[1]/text()' ) as companybook,
        EXTRACTVALUE(xmlrecord,'/row/c24[1]/text()' ) as accountofficerid,
        EXTRACTVALUE(xmlrecord,'/row/c25[1]/text()' ) as otherofficerid,
        EXTRACTVALUE(xmlrecord,'/row/c46[1]/text()' ) as postingrestrictionid,
        EXTRACTVALUE(xmlrecord,'/row/c47[1]/text()' ) as postingrestrictionname,
        EXTRACTVALUE(xmlrecord,'/row/c129[1]/text()' ) as riskrating,
        EXTRACTVALUE(xmlrecord,'/row/c48/text()' ) as branch_code,
        EXTRACTVALUE(xmlrecord,'/row/c185/text()' ) as authoriser_name,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="23"][1]/text()' ) as bank_relation,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="3"][1]/text()' ) as birth_province,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="142"][1]/text()' ) as bk_customer_id,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="165"][1]/text()' ) as bk_eco_sub_sect,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="130"][1]/text()' ) as bk_education,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="28"][1]/text()' ) as nextofkin,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="29"][1]/text()' ) as bk_next_kin_tel,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="30"][1]/text()' ) as bk_next_kin_email,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="31"][1]/text()' ) as bk_next_kin_id_no,     
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="35"][1]/text()' ) as bk_sal_range, 
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="12"][1]/text()' ) as cell_name, 
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="12"][1]/text()' ) as district_name,
        EXTRACTVALUE(xmlrecord,'/row/c46[1]' ) as POSTING_RESTRICT,
        EXTRACTVALUE(xmlrecord,'/row/c30[1]/text()' ) as countryofresidence,
        EXTRACTVALUE(xmlrecord,'/row/c28[1]/text()' ) as nationality,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="17"][1]' ) as PROVINCE,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="13"][1]' ) as DISTRICT,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="20"][1]' ) as SECTOR_ID,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="12"][1]' ) as CELL_ID,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="18"][1]' ) as VILLAGE_ID,
        EXTRACTVALUE(xmlrecord,'/row/c74[1]' ) as employers_name,
        EXTRACTVALUE(xmlrecord,'/row/c71[1]' ) as employment_status,
        EXTRACT(xmlrecord,'/row/c75' ) as EMPLOYERS_ADD,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="26"][1]' ) as EMPLOY_PHONE,
        EXTRACTVALUE(xmlrecord,'/row/c179[@m="27"][1]' ) as EMPLOY_EMAIL
    FROM T24.FBNK_CUSTOMER
"""
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
