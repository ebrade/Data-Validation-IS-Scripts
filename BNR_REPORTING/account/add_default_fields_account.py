import pandas as pd


class AddDefaultFields():
    def add_default_fields(self):
        CUSTOMER_DATA = pd.read_csv("BUSINESSREPORT/DATA/SOURCE/ACCOUNT_ORACLE_DATA.csv", sep="|", dtype=str)

        ADDITIONAL_COLUMNS = [
            {"column_name": "COUNTRY", "value": "RW"}, 
            {"column_name": "LE_BOOK", "value": "040"},
            {"column_name": "INT RATE DR", "value": "0"}, 
            {"column_name": "INT RATE DR", "value": "0"},
            {"column_name": "ACCOUNT_CLOSING_DATE", "value": "01-JAN-1900"},
            {"column_name": "ACCOUNT_OWNERSHIP", "value": "O"},
            {"column_name": "CARD_SUBSCRIPTION", "value": "N"},
             
        ]

        for col in ADDITIONAL_COLUMNS:
            CUSTOMER_DATA[col["column_name"]] = col["value"]


        output_path = "BUSINESSREPORT/DATA/SOURCE/UPDATED_CUSTOMER.csv"
        CUSTOMER_DATA.to_csv(output_path, index=False, sep="|")

