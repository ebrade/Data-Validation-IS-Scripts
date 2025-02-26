from money_transfer_analyzer import MoneyTransferAnalyzer
from datetime import datetime
import time


def main():
    start_t = time.time()
    st_time = datetime.now()
    money_transfer_analyzer_obj = MoneyTransferAnalyzer(
      cols=['COUNTRY', 'LE BOOK', 'BUSINESS DATE', 'MTO LIST', 'REMITTANCE TYPE',
       'CUSTOMER NAME', 'ID TYPE', 'IDENTIFICATION NUMBER',
       'OTHER PARTY NAME', 'OTHER ID NUMBER',
       'RESIDENTS FLAG', 'REMITTANCE COUNTRY', 'CURRENCY',
       'TRANSACTION PURPOSE', 'AMOUNT LCY', 'AMOUNT FCY',
       'FEES AND COMMISSION'],
      file_checked="MONEY_TRANSFER",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="SEQUENCE NUMBER"
    )
    # Fields to be added: 'VISION GL',

    money_transfer_analyzer_obj.load_destination_data()
    money_transfer_analyzer_obj.load_source_data()
    money_transfer_analyzer_obj.check_accuracy()
    money_transfer_analyzer_obj.export_exceptions()

    print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
    print(f"Starting time: {st_time}  End time: {datetime.now()}")

if __name__ == "__main__":
  main()