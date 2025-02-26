import pandas as pd


class AddDefaultFields():
    def add_default_fields(self):
        CUSTOMER_DATA = pd.read_csv("../Data/Source/BOUNCE_CHEQUE_ORACLE_DATA.csv", sep="|", dtype=str)

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY", "value": "RW"},
            {"column_name": "LE_BOOK", "value": "040"},
            {"column_name": "DECLARATION_DATE", "value": "01-JAN-1900"}
        ]

        for col in ADDITIONAL_COLUMNS:
            CUSTOMER_DATA[col["column_name"]] = col["value"]


        output_path = "../Data/Source/UPDATED_BOUNCE_CHEQUE.csv"
        CUSTOMER_DATA.to_csv(output_path, index=False, sep="|")

