import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
import pandas as pd
import time
from datetime import datetime
from is_data_validation.db_connector import DBConnector


start_t = time.time()
st_time = datetime.now()

oracle_query = """
SELECT 
    x.RECID AS Contract_ID,
    x.Customer_ID,
    x.Vision_OUC,
    x.Currency,
    x.PRODUCT_LINE,
    x.PRODUCT_GROUP,
    x.PRODUCT,
    x.Contract_Status,
    x.Orig_Contract_Date,
    x.Start_Date,
    y.Maturity_Date,
    x.Arr_Account
FROM (
    -- Extract fields from the XML record in FBNK_AA_ARRANGEMENT
    SELECT 
        arr.RECID,  -- Ensure RECID is selected
        xt.Customer_ID,
        xt.Vision_OUC,
        xt.Currency,
        xt.PRODUCT_LINE,
        xt.PRODUCT_GROUP,
        xt.PRODUCT,
        xt.Contract_Status,
        xt.Orig_Contract_Date,
        xt.Start_Date,
        xt.Arr_Account
    FROM T24.FBNK_AA_ARRANGEMENT arr
    JOIN XMLTABLE(
        '/row' PASSING arr.xmlrecord
        COLUMNS 
            Customer_ID VARCHAR2(100) PATH 'c1[1]/text()',
            Vision_OUC VARCHAR2(100) PATH 'c9[1]/text()',
            Currency VARCHAR2(100) PATH 'c8[1]/text()',
            PRODUCT_LINE VARCHAR2(100) PATH 'c15[1]/text()',
            PRODUCT_GROUP VARCHAR2(100) PATH 'c16[1]/text()',
            PRODUCT VARCHAR2(100) PATH 'c17[1]/text()',
            Contract_Status VARCHAR2(100) PATH 'c11[1]/text()',
            Orig_Contract_Date VARCHAR2(100) PATH 'c24[1]/text()',
            Start_Date VARCHAR2(100) PATH 'c12[1]/text()',
            Arr_Account VARCHAR2(100) PATH 'c14[1]/text()'
    ) xt ON xt.PRODUCT_LINE = 'LENDING' -- Early filtering
) x
LEFT JOIN T24.FBNK_AA_ACCOUNT_DET001 aa_acc 
    ON x.RECID = aa_acc.RECID  -- Now RECID exists in x
LEFT JOIN XMLTABLE(
    '/row' PASSING aa_acc.xmlrecord
    COLUMNS 
        Maturity_Date VARCHAR2(100) PATH 'c6[1]/text()'
) y ON 1=1
"""

ecb_query = """
SELECT 
    a.RECID AS Arr_Account,
    key_data.CONSOL_KEY,
    NVL(MAX(CASE 
                WHEN c13_data.CURR_ASSET_TYPE = 'CURACCOUNT' THEN eb.PRINCIPAL_AMOUNT
                ELSE NULL
            END), '0') AS CURACCOUNT_BALANCE,
    NVL(MAX(CASE 
                WHEN c13_data.CURR_ASSET_TYPE = 'TOTCOMMITMENTBL' THEN eb.PRINCIPAL_AMOUNT
                ELSE NULL
            END), '0') AS TOTCOMMITMENTBL_BALANCE
FROM (
    SELECT a.RECID, a.XMLRECORD
    FROM T24.FBNK_EB_CONTRACT_BA001 a
    WHERE {where_clause}
) a
JOIN XMLTABLE(
    '/row' PASSING a.XMLRECORD
    COLUMNS 
        CONSOL_KEY VARCHAR2(100) PATH 'c14/text()'
) key_data ON 1 = 1
LEFT JOIN XMLTABLE(
    '/row/c13' PASSING a.XMLRECORD
    COLUMNS 
        CURR_ASSET_TYPE VARCHAR2(100) PATH 'text()', 
        M_ATTR VARCHAR2(10) PATH '@m'
) c13_data ON 1 = 1
LEFT JOIN XMLTABLE(
    '/row/c5' PASSING a.XMLRECORD
    COLUMNS 
        M_ATTR VARCHAR2(10) PATH '@m',
        PRINCIPAL_AMOUNT VARCHAR2(100) PATH 'text()'
) eb ON NVL(c13_data.M_ATTR, '1') = NVL(eb.M_ATTR, '1')
GROUP BY a.RECID, key_data.CONSOL_KEY
ORDER BY a.RECID
"""

interest_qry ="""
WITH ExtractedData AS (
    SELECT 
        SUBSTR(RECID, 1, INSTR(RECID, '-', 1, 1) - 1) AS PREFIX_RECID,
        CASE 
            WHEN RECID LIKE '%-PENALTYINT-%' THEN 'PENALTY_INTEREST'
            WHEN RECID LIKE '%-PRINCIPALINT-%' THEN 'PRINCIPAL_INTEREST'
        END AS INTEREST_TYPE,
        EXTRACTVALUE(XMLRECORD, '/row/c27[1]/text()') AS EFFECTIVE_RATE,
        TO_NUMBER(SUBSTR(RECID, INSTR(RECID, '.', -1) + 1)) AS CurrNo
    FROM T24.FBNK_AA_ARR_INTEREST WHERE {where_clause}
),
RankedData AS (
    SELECT 
        PREFIX_RECID,
        INTEREST_TYPE,
        EFFECTIVE_RATE,
        CurrNo,
        ROW_NUMBER() OVER (
            PARTITION BY PREFIX_RECID, INTEREST_TYPE
            ORDER BY CurrNo DESC
        ) AS rn
    FROM ExtractedData
)
SELECT 
    PREFIX_RECID AS CONTRACT_ID,
    MAX(CASE WHEN INTEREST_TYPE = 'PENALTY_INTEREST' THEN EFFECTIVE_RATE END) AS PENALTY_INTEREST,
    MAX(CASE WHEN INTEREST_TYPE = 'PRINCIPAL_INTEREST' THEN EFFECTIVE_RATE END) AS PRINCIPAL_INTEREST
FROM RankedData
WHERE rn = 1
GROUP BY PREFIX_RECID

"""

class T24ContractFetcher():
    def __init__(self):
        self.con_query = oracle_query
        self.ecb_query = ecb_query
        self.lending_df = None
    def fetch_contarct_info(self):
        db_conn = DBConnector(oracle_query=self.con_query)
        lending_info = db_conn.fetch_oracle_data()
        self.lending_df = pd.DataFrame(lending_info["data"], columns=lending_info["cols"])
        
    def fetch_payment_frequencies(self, recid_prefix_list, db_conn):
        """
        Fetches the payment frequencies for given RECID prefixes.
        """
        query = """
        WITH RANKED_DATA AS (
            SELECT 
                EXTRACT(XMLRECORD, '/row/c84[1]/text()').getStringVal() AS CONTRACT_ID,
                COALESCE(
                    EXTRACT(XMLRECORD, '/row/c18[2]/text()').getStringVal(),
                    EXTRACT(XMLRECORD, '/row/c18[1]/text()').getStringVal()
                ) AS PAYMENT_FREQUENCY,
                ROW_NUMBER() OVER (
                    PARTITION BY EXTRACT(XMLRECORD, '/row/c84[1]/text()').getStringVal()
                    ORDER BY RECID DESC  -- Ensures we get the latest RECID per contract
                ) AS RN
            FROM T24.FBNK_AA_ARR_PAYMENT001
            WHERE {where_clause}
        )
        SELECT CONTRACT_ID, PAYMENT_FREQUENCY FROM RANKED_DATA WHERE RN = 1
        """

        db_conn.oracle_query = query
        result = db_conn.fetch_oracle_data_in_batches(recid_prefix_list, query)

        return pd.DataFrame(result["data"], columns=result["cols"])
    
    def fetch_eb_contacts(self):
        multi_var_cols = ["CURR_ASSET_TYPE", "TYPE_SYSDATE","MATURITY_DATE", "OPEN_BALANCE"]
        db_conn = DBConnector(oracle_query=self.ecb_query)
        
        account_list = self.lending_df["ARR_ACCOUNT"].to_list()
        arrangement_id_list = self.lending_df["CONTRACT_ID"].to_list()
        # Split the list into chunks of 500
        chunk_size = 500
        chunks = [account_list[i:i + chunk_size] for i in range(0, len(account_list), chunk_size)]
        arr_chunks = [arrangement_id_list[i:i + chunk_size] for i in range(0, len(arrangement_id_list), chunk_size)]
        frequency_list=[]
        cols_freq = []
        
        for arr_chunk in arr_chunks:
            chunk_frequencies = self.fetch_payment_frequencies(arr_chunk, db_conn)
            frequency_list.append(chunk_frequencies)
        loan_frequencies = pd.concat(frequency_list, ignore_index=True) if frequency_list else pd.DataFrame()
        ecb_df_list = []
        for chunk in chunks:
            
            chunk_result = db_conn.fetch_oracle_data_in_batches(recid_prefix_list=chunk, query=ecb_query)
            ecb_df_list.append(pd.DataFrame(chunk_result['data'], columns=chunk_result['cols']))
        interest_df_list = []
        for arr_chunk in arr_chunks:
            chunk_result = db_conn.fetch_oracle_data_in_batches(recid_prefix_list=arr_chunk, query=interest_qry)
            interest_df_list.append(pd.DataFrame(chunk_result['data'], columns=chunk_result['cols']))
        ecb_df = pd.concat(ecb_df_list)
        interest_df = pd.concat(interest_df_list)
        df = pd.merge(self.lending_df, ecb_df, on=['ARR_ACCOUNT'], how='left')
        contract_df = pd.merge(df, loan_frequencies, on='CONTRACT_ID', how='left')
        contract_df = pd.merge(contract_df, interest_df, on='CONTRACT_ID', how='left')
        return contract_df
            
        

start_t = time.time()
t24_con_ins = T24ContractFetcher()
t24_con_ins.fetch_contarct_info()
ecb_df = t24_con_ins.fetch_eb_contacts()
ecb_df.to_csv('../Data/Source/CONTRACT_INFORMATION.csv',index=False)
print(ecb_df)
print(f"Finished fetching Oracle data in {time.time() - start_t:.2f} secs.")
