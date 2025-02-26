import pandas as pd


class AddDefaultFields():
    def add_default_fields(self):
        CUSTOMER_DATA = pd.read_csv("../Data/Source/CONTRACT_DISBURSED_ORACLE_DATA.csv", sep="|", dtype=str)

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY", "value": "RW"},
            {"column_name": "LE_BOOK", "value": "01"},
        ]

        for col in ADDITIONAL_COLUMNS:
            CUSTOMER_DATA[col["column_name"]] = col["value"]

        output_path = "../Data/Source/UPDATED_CONTRACT_DISBURSED.csv"
        CUSTOMER_DATA.to_csv(output_path, index=False, sep="|")

