import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.BUSINESS_REPORTING.contract_schedule.analyzer_contract_schedule import  ContractScheduleAnalyzer


def main():
    contract_disbursed_analyzer_obj = ContractScheduleAnalyzer(
      cols=[
        'INT_AMOUNT_DUE_LCY',
        'INT_AMOUNT_DUE_FCY',
        'PRINCIPAL_AMOUNT_PAID_LCY',
        'PRINCIPAL_AMOUNT_PAID_FCY',
        'INT_AMOUNT_PAID_LCY',
        'INT_AMOUNT_PAID_FCY',
        'OUTSTANDING_AMOUNT_LCY',
        'OUTSTANDING_AMOUNT_FCY',
        'PRINCIPAL_AMOUNT_DUE_FCY',
        'PRINCIPAL_AMOUNT_DUE_LCY',
        'PAYMENT_DATE',
        'SCHEDULE_DATE',
        'YEAR_MONTH',
        'COUNTRY',
        'LE_BOOK',
        'CONTRACT_ID'
      ],
      file_checked="CONTRACT_SCHEDULE",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="RECID"
    )
  
    contract_disbursed_analyzer_obj.load_destination_data()
    contract_disbursed_analyzer_obj.load_source_data()
    contract_disbursed_analyzer_obj.check_accuracy()
    contract_disbursed_analyzer_obj.export_exceptions()

if __name__ == "__main__":
  main()