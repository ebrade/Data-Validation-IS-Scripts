from currency_analyzer import CurrencyAnalyzer
from datetime import datetime
import time


def main():
    start_t = time.time()
    st_time = datetime.now()
    currency_analyzer_obj = CurrencyAnalyzer(
      cols=['COUNTRY', 'LE BOOK', 'BUSINESS DATE', 'MID RATE',
       'BUY RATE', 'SELL RATE', 'TRANSFER MID RATE', 'TRANSFER BUY RATE',
       'TRANSFER SELL RATE'
       ],
      file_checked="CURRENCY_RATES",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="CURRENCY"
    )
    # Fields to be added: 'VISION GL',

    currency_analyzer_obj.load_destination_data()
    currency_analyzer_obj.load_source_data()
    currency_analyzer_obj.check_accuracy()
    currency_analyzer_obj.export_exceptions()

    print("--- Processed in %.2f seconds ---" % (time.time() - start_t))
    print(f"Starting time: {st_time}  End time: {datetime.now()}")

if __name__ == "__main__":
  main()