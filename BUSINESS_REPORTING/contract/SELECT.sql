WITH RankedData AS (
    SELECT 
        RECID,
        SUBSTR(RECID, 1, INSTR(RECID, '-', 1, 1) - 1) AS PREFIX_RECID,
        CASE 
            WHEN RECID LIKE '%-PENALTYINT-%' THEN 'PENALTY_INTEREST'
            WHEN RECID LIKE '%-PRINCIPALINT-%' THEN 'PRINCIPAL_INTEREST'
        END AS INTEREST_TYPE,
        EFFECTIVE_RATE,
        ROW_NUMBER() OVER (
            PARTITION BY SUBSTR(RECID, 1, INSTR(RECID, '-', 1, 1) - 1),
                         CASE 
                             WHEN RECID LIKE '%-PENALTYINT-%' THEN 'PENALTY_INTEREST'
                             WHEN RECID LIKE '%-PRINCIPALINT-%' THEN 'PRINCIPAL_INTEREST'
                         END
            ORDER BY RECID DESC -- Uses natural order assuming eldest → latest
        ) AS rn
    FROM your_table
)
SELECT 
    RECID,
    PREFIX_RECID,
    MAX(CASE WHEN INTEREST_TYPE = 'PENALTY_INTEREST' THEN EFFECTIVE_RATE END) AS PENALTY_INTEREST,
    MAX(CASE WHEN INTEREST_TYPE = 'PRINCIPAL_INTEREST' THEN EFFECTIVE_RATE END) AS PRINCIPAL_INTEREST
FROM RankedData
WHERE rn = 1
GROUP BY RECID, PREFIX_RECID;






WITH CURACCOUNT_Data AS (
    SELECT 
        a.RECID AS Arr_Account, 
        key_data.CONSOL_KEY,
        c13_data.CURR_ASSET_TYPE,
        NVL(eb.PRINCIPAL_AMOUNT, '0') AS CURACCOUNT_BALANCE
    FROM T24.FBNK_EB_CONTRACT_BA001 a
    CROSS JOIN XMLTABLE(
        '/row' PASSING a.XMLRECORD
        COLUMNS 
            CONSOL_KEY VARCHAR2(100) PATH 'c14/text()'
    ) key_data
    CROSS JOIN XMLTABLE(
        '/row/c13[text()="CURACCOUNT"]' PASSING a.XMLRECORD
        COLUMNS 
            CURR_ASSET_TYPE VARCHAR2(100) PATH 'text()',
            M_ATTR VARCHAR2(10) PATH '@m'
    ) c13_data
    LEFT JOIN XMLTABLE(
        '/row/c5' PASSING a.XMLRECORD
        COLUMNS 
            M_ATTR VARCHAR2(10) PATH '@m',
            PRINCIPAL_AMOUNT VARCHAR2(100) PATH 'text()'
    ) eb
    ON NVL(c13_data.M_ATTR, '1') = NVL(eb.M_ATTR, '1')
),
TOTCOMMITMENTBL_Data AS (
    SELECT 
        a.RECID AS Arr_Account, 
        key_data.CONSOL_KEY,
        c13_data.CURR_ASSET_TYPE,
        NVL(eb.PRINCIPAL_AMOUNT, '0') AS TOTCOMMITMENTBL_BALANCE
    FROM T24.FBNK_EB_CONTRACT_BA001 a
    CROSS JOIN XMLTABLE(
        '/row' PASSING a.XMLRECORD
        COLUMNS 
            CONSOL_KEY VARCHAR2(100) PATH 'c14/text()'
    ) key_data
    CROSS JOIN XMLTABLE(
        '/row/c13[text()="TOTCOMMITMENTBL"]' PASSING a.XMLRECORD
        COLUMNS 
            CURR_ASSET_TYPE VARCHAR2(100) PATH 'text()',
            M_ATTR VARCHAR2(10) PATH '@m'
    ) c13_data
    LEFT JOIN XMLTABLE(
        '/row/c5' PASSING a.XMLRECORD
        COLUMNS 
            M_ATTR VARCHAR2(10) PATH '@m',
            PRINCIPAL_AMOUNT VARCHAR2(100) PATH 'text()'
    ) eb
    ON NVL(c13_data.M_ATTR, '1') = NVL(eb.M_ATTR, '1')
)
SELECT 
    a.Arr_Account,
    a.CONSOL_KEY,
    NVL(a.CURACCOUNT_BALANCE, '0') AS CURACCOUNT_BALANCE,
    NVL(b.TOTCOMMITMENTBL_BALANCE, '0') AS TOTCOMMITMENTBL_BALANCE
FROM CURACCOUNT_Data a
LEFT JOIN TOTCOMMITMENTBL_Data b
ON a.Arr_Account = b.Arr_Account
WHERE ROWNUM<10;  -- Filter added here

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
    WHERE ROWNUM<1000
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
ORDER BY a.RECID;












WITH ExtractedData AS (
    SELECT 
        a.RECID AS Arr_Account, 
        key_data.CONSOL_KEY,
        c13_data.CURR_ASSET_TYPE,
        NVL(eb.PRINCIPAL_AMOUNT, '0') AS PRINCIPAL_AMOUNT
    FROM (
        SELECT * FROM T24.FBNK_EB_CONTRACT_BA001 WHERE RECID = '100179864449'
    ) a  -- ✅ EARLY FILTERING
    CROSS JOIN XMLTABLE(
        '/row' PASSING a.XMLRECORD
        COLUMNS 
            CONSOL_KEY VARCHAR2(100) PATH 'c14/text()'
    ) key_data
    CROSS JOIN XMLTABLE(
        '/row/c13[text()="CURACCOUNT"]' PASSING a.XMLRECORD
        COLUMNS 
            CURR_ASSET_TYPE VARCHAR2(100) PATH 'text()',
            M_ATTR VARCHAR2(10) PATH '@m'
    ) c13_data
    LEFT JOIN XMLTABLE(
        '/row/c5' PASSING a.XMLRECORD
        COLUMNS 
            M_ATTR VARCHAR2(10) PATH '@m',
            PRINCIPAL_AMOUNT VARCHAR2(100) PATH 'text()'
    ) eb
    ON NVL(c13_data.M_ATTR, '1') = NVL(eb.M_ATTR, '1')
)
SELECT * FROM ExtractedData;




SELECT 
    arr.RECID AS Contract_ID,
    x.Customer_ID,
    x.Vision_OUC,
    x.Vision_SBU,
    x.Currency,
    x.PRODUCT_LINE,
    x.PRODUCT_GROUP,
    x.Contract_Status,
    x.Orig_Contract_Date,
    x.Start_Date,
    y.Maturity_Date,
    x.Arr_Account
FROM T24.FBNK_AA_ARRANGEMENT arr
LEFT JOIN T24.FBNK_AA_ACCOUNT_DET001 aa_acc 
    ON arr.RECID = aa_acc.RECID


-- Extract fields from the XML record in FBNK_AA_ARRANGEMENT
JOIN XMLTABLE(
    '/row' PASSING arr.xmlrecord
    COLUMNS 
        Customer_ID VARCHAR2(100) PATH 'c1[1]/text()',
        Vision_OUC VARCHAR2(100) PATH 'c9[1]/text()',
        Vision_SBU VARCHAR2(100) PATH 'c162[1]/text()',
        Currency VARCHAR2(100) PATH 'c8[1]/text()',
        PRODUCT_LINE VARCHAR2(100) PATH 'c15[1]/text()',
        PRODUCT_GROUP VARCHAR2(100) PATH 'c16[1]/text()',
        Contract_Status VARCHAR2(100) PATH 'c11[1]/text()',
        Orig_Contract_Date VARCHAR2(100) PATH 'c24[1]/text()',
        Start_Date VARCHAR2(100) PATH 'c12[1]/text()',
        Arr_Account VARCHAR2(100) PATH 'c14[1]/text()'
) x ON 1=1

-- Extract Maturity_Date from FBNK_AA_ACCOUNT_DET001 XML
LEFT JOIN XMLTABLE(
    '/row' PASSING aa_acc.xmlrecord
    COLUMNS 
        Maturity_Date VARCHAR2(100) PATH 'c6[1]/text()'
) y ON 1=1

WHERE x.PRODUCT_LINE = 'LENDING' and ROWNUM<100;





SELECT 
    a.RECID, 
    eb.CONSOL_KEY,
    eb.OPEN_BALANCE
FROM T24.FBNK_EB_CONTRACT_BA001 a,
     XMLTABLE('/row' PASSING a.XMLRECORD
              COLUMNS 
                 CONSOL_KEY VARCHAR2(100) PATH 'c14/text()',
                 OPEN_BALANCE VARCHAR2(100) PATH 'c5/text()'
              ) eb
WHERE existsNode(a.XMLRECORD, '/row/c13[text()="CURACCOUNT"]') > 0 and  a.RECID='100057143098';


WITH RECID_DATA AS (
    SELECT
        RECID,
        SUBSTR(RECID, 1, INSTR(RECID, '-') - 1) AS RECID_PREFIX,  -- Extract the prefix (e.g., AA21284HLP75)
        TO_DATE(SUBSTR(RECID, INSTR(RECID, 'SCHEDULE-') + 9, 8), 'YYYYMMDD') AS SCHEDULE_DATE,  -- Extract and convert the date
        EXTRACTVALUE(XMLRECORD, '/row/c18[2]/text()') AS PAYMENT_FREQUENCY
    FROM
        T24.FBNK_AA_ARR_PAYMENT001
        WHERE RECID LIKE 'AA21288292CZ%'
),
RANKED_DATA AS (
    SELECT
        RECID,
        RECID_PREFIX,
        SCHEDULE_DATE,
        PAYMENT_FREQUENCY,
        ROW_NUMBER() OVER (PARTITION BY RECID_PREFIX ORDER BY SCHEDULE_DATE DESC) AS RN  -- Rank records by date within each prefix
    FROM
        RECID_DATA
)
SELECT
RECID,
    RECID_PREFIX,
    PAYMENT_FREQUENCY
FROM
    RANKED_DATA
WHERE
    RN = 1;  -- Get the latest record for each prefix

SELECT * FROM T24.FBNK_AA_ARR_PAYMENT001 WHERE RECID LIKE 'AA2128863K5Y%';

WITH RECID_DATA AS (
    SELECT
        RECID,
        EXTRACTVALUE(XMLRECORD, '/row/c18[2]/text()') AS PAYMENT_FREQUENCY,
        EXTRACTVALUE(XMLRECORD, '/row/c84[1]/text()') AS CONTRACT_ID
    FROM
        T24.FBNK_AA_ARR_PAYMENT001
    WHERE
        ROWNUM<100
),
RANKED_DATA AS (
    SELECT
        CONTRACT_ID,
        PAYMENT_FREQUENCY,
        ROW_NUMBER() OVER (PARTITION BY CONTRACT_ID ORDER BY RECID DESC) AS RN  -- Rank records by RECID within each prefix
    FROM
        RECID_DATA
)
SELECT
    CONTRACT_ID,
    PAYMENT_FREQUENCY
FROM
    RANKED_DATA
WHERE
    RN = 1;  -- Get the latest record for each contract


