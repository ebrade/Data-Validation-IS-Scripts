import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.BUSINESS_REPORTING.bounce_cheque.analyzer_bounce_cheque import  BounceChequeAnalyzer


def main():
    bounce_cheque_analyzer_obj = BounceChequeAnalyzer(
      cols=['BUSINESS_DATE',
        'ACCOUNT_NO',
        'CHEQUE_NO',
        'CHEQUE_ISSUED_DATE',
        'CURRENCY',
        'CHEQUE_AMOUNT_FCY',
        'BOUNCE_CHEQUE_REASON',
        'BENEFICIARY',
        'COUNTRY',
        'LE_BOOK'
      ],
      file_checked="BOUNCE_CHEQUE",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="RECID"
    )
  
    bounce_cheque_analyzer_obj.load_destination_data()
    bounce_cheque_analyzer_obj.load_source_data()
    bounce_cheque_analyzer_obj.check_accuracy()
    bounce_cheque_analyzer_obj.export_exceptions()

if __name__ == "__main__":
  main()