from account_analyzer import AccountAnalyzer
from datetime import datetime
import time


def main():
    start_t = time.time()
    st_time = datetime.now()
    account_analyzer_obj = AccountAnalyzer(
      cols=['COUNTRY', 'LE BOOK', 'ACCOUNT NAME', 'VISION OUC',
       'VISION SBU', 'ACCOUNT STATUS', 'ACCOUNT STATUS DATE', 'CUSTOMER ID',
       'ACCOUNT OFFICER', 'CURRENCY', 'ACCOUNT TYPE',
       'ACCOUNT OPEN DATE', 'ACCOUNT CLOSING DATE', 'FREEZE STATUS',
       'INT RATE DR','ECONOMIC SUB SECTOR CODE',
       'ECONOMIC SUB SECTOR CODE ISIC', 'PUBLIC SECTOR CODE',
       'INSTITUTIONAL SECTOR CODE', 'LAST TRANSACTION DATE',
       'ACCOUNT OWNERSHIP', 'JOINT PARTICIPANT COUNT', 'CARD SUBSCRIPTION',
       'PERFORMANCE CLASS', 'CREDIT CATEGORY',
       'DATE LAST MODIFIED', 'ECONOMIC SECTOR CODE'],
      file_checked="ACCOUNT",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="ACCOUNT NO"
    )
    # Fields to be added: 'VISION GL',

    account_analyzer_obj.load_destination_data()
    account_analyzer_obj.load_source_data()
    account_analyzer_obj.check_accuracy()
    account_analyzer_obj.export_exceptions()

    print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
    print(f"Starting time: {st_time}  End time: {datetime.now()}")

if __name__ == "__main__":
  main()