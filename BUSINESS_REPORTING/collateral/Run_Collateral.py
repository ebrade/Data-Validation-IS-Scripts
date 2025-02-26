from collateral_analyzer import CollateralAnalyzer
from datetime import datetime
import time


def main():
    start_t = time.time()
    st_time = datetime.now()
    collateral_analyzer_obj = CollateralAnalyzer(
      cols=['COUNTRY', 'LE BOOK', 'CUSTOMER ID',
       'COLLATERAL TYPE', 'COLLATERAL OWNERSHIP', 'COLLATERAL AMOUNT LCY',
       'COLLATERAL LAST VALUATION DATE', 'COLLATERAL EXPIRY DATE',
       'COLLATERAL DISCOUNT AMT LCY', 'COLLATERAL DISCOUNT RATE',
       'COLLATERAL MARKET VALUE', 'UPI NUMBER', 'NAME PROPERTY VALUER',
       'REG NUMBER VALUER', 'RDB REG NUMBER', 'LTV RATIO', 'INSURED',
       'INSURANCE EXPIRY DATE', 'GAURANTEE ISSUER', 'DATE LAST MODIFIED'],
      file_checked="COLLATERAL",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="COLLATERAL ID"
    )
    # Fields to be added: 'VISION GL',

    collateral_analyzer_obj.load_destination_data()
    collateral_analyzer_obj.load_source_data()
    collateral_analyzer_obj.check_accuracy()
    collateral_analyzer_obj.export_exceptions()

    print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
    print(f"Starting time: {st_time}  End time: {datetime.now()}")

if __name__ == "__main__":
  main()