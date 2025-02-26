import pandas as pd


class AddDefaultFields():
    def add_default_fields(self):
        CUSTOMER_DATA = pd.read_csv("../Data/Source/BRANCH_INFO_ORACLE_DATA.csv", sep="|", dtype=str)

        ADDITIONAL_COLUMNS = [
            {"column_name": "FEED_DATE", "value": "NULL"}, 
            {"column_name": "FEED_STATUS", "value": "N"},
            {"column_name": "COUNTRY", "value": "RW"},
            {"column_name": "LE_BOOK", "value": "1"},
            {"column_name": "BRANCH_CATEGORY", "value": "2"}

        ]

        for col in ADDITIONAL_COLUMNS:
            CUSTOMER_DATA[col["column_name"]] = col["value"]


        output_path = "../Data/Source/UPDATED_BRANCH_INFO.csv"
        CUSTOMER_DATA.to_csv(output_path, index=False, sep="|")

