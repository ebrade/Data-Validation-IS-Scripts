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
SELECT RECID,
        EXTRACTVALUE(xmlrecord,'/row/c9/text()') AS Vision_OUC,
        EXTRACTVALUE(xmlrecord,'/row/c162/text()') AS Vision_SBU,
        EXTRACTVALUE(xmlrecord,'/row/c24/text()') AS Orig_Contract_Date,
        EXTRACTVALUE(xmlrecord,'/row/c12[1]/text()') AS Start_Date,

        EXTRACTVALUE(aa_acc.xmlrecord,'/row/c6[1]/text()' ) as Maturity_Date,
        EXTRACTVALUE(xmlrecord,'/row/c162/text()') AS Settlement_Date,

        EXTRACTVALUE(xmlrecord,'/row/c162/text()') AS Settlement_Date,


  
           
    FROM T24.FBNK_AA_ARRANGEMENT
    left join T24.FBNK_AA_ACCOUNT_DET001 aa_acc on arr.recid=aa_acc.recid
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









select arr.RECID as arrangement_id,
        EXTRACTVALUE(arr.XMLRECORD,'/row/c14[1]/text()' ) as arrangement_account_number,
        EXTRACTVALUE(arr.XMLRECORD,'/row/c11[1]/text()' ) as arrangement_status,
        EXTRACT(arr.XMLRECORD,'/row/c17' ) as arrangement_type,
        EXTRACTVALUE(arr.XMLRECORD,'/row/c15[1]/text()' ) as arrangement_product_line,
        EXTRACTVALUE(aa_acc.XMLRECORD,'/row/c6[1]/text()' ) as arrangement_maturity_date,
        EXTRACTVALUE(arr.XMLRECORD,'/row/c9[1]/text()' ) as arrangement_branch_code,
        EXTRACTVALUE(aa_acc.XMLRECORD,'/row/c68[1]/text()' ) as arrangement_amount,
        EXTRACTVALUE(aa_acc.XMLRECORD,'/row/c70[1]/text()' ) as ARR_DORMANCY_STATUS,
        EXTRACTVALUE(arr.XMLRECORD,'/row/c12[1]/text()' ) as arrangement_start_date,
        EXTRACT(arr.XMLRECORD,'/row/c1' ) as arrangement_customer
       
    from T24.FBNK_AA_ARRANGEMENT arr
    left join T24.FBNK_AA_ACCOUNT_DET001 aa_acc on arr.recid=aa_acc.recid
