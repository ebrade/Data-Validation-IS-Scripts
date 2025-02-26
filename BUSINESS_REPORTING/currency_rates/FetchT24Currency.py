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
select RECID as Currency,
          EXTRACTVALUE(xmlrecord,'/row/c60[1]/text()') AS Business_Date,
          EXTRACTVALUE(xmlrecord,'/row/c14[@m=2]/text()') AS Mid_Rate,
          EXTRACTVALUE(xmlrecord,'/row/c14[@m=3]/text()') AS Transfer_Mid_Rate,
          EXTRACTVALUE(xmlrecord,'/row/c16[@m=2]/text()') AS Buy_Rate,
          EXTRACTVALUE(xmlrecord,'/row/c16[@m=3]/text()') AS Transfer_Buy_Rate,
          EXTRACTVALUE(xmlrecord,'/row/c17[@m=2]/text()') AS Sell_Rate,
          EXTRACTVALUE(xmlrecord,'/row/c17[@m=3]/text()') AS Transfer_Sell_Rate
from T24.FBNK_CURRENCY
"""
db_con = DBConnector(oracle_query=oracle_query)
f_ins = FieldsAnalyzer(cols_to_check=None, 
                       is_post_cob=IS_POST_COB,
                       file_checked="Currency_Rates",
                       test_iter=TEST_ITERATION)
print('Connected to DB.........................')
result = db_con.fetch_oracle_multi_value()
oracle_data = pd.DataFrame(result["data"], columns=result["cols"])
# root_folder = f_ins.construct_root()
oracle_data.to_csv(f"../Data/Source/{f_ins.file_checked}_ORACLE_DATA_OG.csv", index=False, sep="|")

print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
print(f"Starting time: {st_time}  End time: {datetime.now()}")
