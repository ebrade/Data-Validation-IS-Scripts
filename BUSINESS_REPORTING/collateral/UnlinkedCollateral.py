import pandas as pd
collateral = pd.read_csv('../Data/Source/COLLATERAL.csv', dtype=str,sep=',')
collateral_right = pd.read_csv('../Data/Source/COLLATERAL_RIGHT_ORACLE_DATA_OG.csv', dtype=str,sep='|')
collateral_right.columns=collateral_right.columns.str.replace('_',' ')
collateral_right=collateral_right[['RECID','LIMIT REFERENCE','ARRANGEMENT']]
# collateral['COLLATERAL ID']=collateral['COLLATERAL ID'].str[:-2]
merged = collateral.merge(collateral_right, left_on='COLL RIGHT', right_on='RECID', how='inner')


unlinked= merged[(merged['LIMIT REFERENCE'].isna())&(merged['ARRANGEMENT'].isna())]
# print(f'len coll: {len(collateral)}')
# print(f'len coll right: {len(collateral_right)}')
# print(unlinked)

unlinked.to_csv('../DATA/Destination/COLLATERAL_UNLINKED.csv', index=False, sep=',')


# merged.to_csv('../DATA/Source/COLLATERAL_Unlinked.csv', index=False, sep=',')

