import pandas as pd


class AddDefaultFields():
    def add_default_fields(self):
        CUSTOMER_DATA = pd.read_csv("../Data/Source/CUSTOMER_ORACLE_DATA.csv", sep="|", dtype=str)

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY_", "value": "RW"}, 
            {"column_name": "LE_BOOK", "value": "040"},
            {"column_name": "FAX_NUMBER_1", "value": "NA"},
            {"column_name": "FAX_NUMBER_2", "value": "NA"},
            {"column_name": "NAICS_CODE", "value": "999999"},
            {"column_name": "SSN_NUMBER", "value": "NULL"}, 
            {"column_name": "HEALTH_INSURANCE_NUMBER", "value": "NULL"}, 
            {"column_name": "EMP_ADDRESS_1", "value": "NULL"}, 
            {"column_name": "EMP_ADDRESS_2", "value": "NULL"}, 
            {"column_name": "EMP_VILLAGE", "value": "NULL"}, 
            {"column_name": "EMP_COUNTRY", "value": "NULL"},
            {"column_name": "WORK_TELEPHONE", "value": "NA"}, 
            {"column_name": "ECONOMIC_SUB_SECTOR_CODE_ISIC", "value": "NA"},
            {"column_name": "ECONOMIC_SUB_SECTOR_CODE", "value": "NA"}
        ]

        for col in ADDITIONAL_COLUMNS:
            CUSTOMER_DATA[col["column_name"]] = col["value"]


        output_path = "../Data/Source/UPDATED_CUSTOMER.csv"
        CUSTOMER_DATA.to_csv(output_path, index=False, sep="|")

