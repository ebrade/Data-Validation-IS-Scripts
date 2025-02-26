import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.BUSINESS_REPORTING.contract_disbursed.analyzer_contract_disbursed import  ContractDisbursedAnalyzer


def main():
    contract_disbursed_analyzer_obj = ContractDisbursedAnalyzer(
      cols=[
        'PREVIOUS_DISBURSED_AMT',
        'CURRENT_DISBURSED_AMT',
        'CURRENCY',
        'COUNTRY',
        'LE_BOOK'
      ],
      file_checked="CONTRACT_DISBURSED",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="CONTRACT_ID"
    )
  
    contract_disbursed_analyzer_obj.load_destination_data()
    contract_disbursed_analyzer_obj.load_source_data()
    contract_disbursed_analyzer_obj.check_accuracy()
    contract_disbursed_analyzer_obj.export_exceptions()

if __name__ == "__main__":
  main()