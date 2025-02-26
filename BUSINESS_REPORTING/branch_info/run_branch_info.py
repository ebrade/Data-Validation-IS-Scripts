import sys
sys.path.append(r"C:\Users\Public\AUDIT_DATA_VALIDATIONS")
from is_data_validation.BUSINESS_REPORTING.branch_info.analyzer_branch_info import  BranchInfoAnalyzer


def main():
    branch_info_analyzer_obj = BranchInfoAnalyzer(
      cols=['OUC_DESCRIPTION',
        'VILLAGE_LIST',
        'BRANCH_CATEGORY',
        'BRANCH_OPEN_DATE',
        'BRANCH_CLOSE_DATE',
        'BRANCH_STATUS',
        'SUB_BRANCH_FLAG',
        'DATE_LAST_MODIFIED'
        # 'FEED_DATE',
        # 'FEED_STATUS',
        # 'BUSINESS_DATE'
      ],
      file_checked="BRANCH_INFO",
      test_iter="ITERATION 1",
      source_name="T24",
      destination_name="SUNOID",
      identifier="VISION_OUC"
    )
  
    branch_info_analyzer_obj.load_destination_data()
    branch_info_analyzer_obj.load_source_data()
    branch_info_analyzer_obj.check_accuracy()
    branch_info_analyzer_obj.export_exceptions()

if __name__ == "__main__":
  main()