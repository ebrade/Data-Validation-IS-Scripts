import numpy as np
from datetime import datetime
import pandas as pd

class MappContract:
    def __init__(self, df):
        self.df = df

    def map_deal_type(self):
        conditions = [
            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'CHARGEOFF.LOAN') & 
            (self.df['PRODUCT'] == 'CHARGED.OFF.LOAN'),
            
            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'CONS.LENDING') & 
            (self.df['PRODUCT'].isin([
                'STAFF.SECURED', 'UNSECURED.PERSONAL.CLIENT', 'RETAIL.USED.VEHICLE.LOAN',
                'CONSUMER.HOME.EQUITY', 'FIXED.INSTALLMENT', 'SECURED.PERSONAL.CLIENT',
                'BKQUICK.LOAN', 'HANDSET.FIN.LOAN', 'RETAIL.NEW.VEHICLE.LOAN'
            ])),

            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'CONS.LENDING') & 
            (self.df['PRODUCT'].isin([
                'STAFF.NEW.VEHICLE.LOAN', 'STAFF.USED.VEHICLE.LOAN', 'STAFF.UNSECURED'
            ])),

            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'EQUIPMENT.LOANS') & 
            (self.df['PRODUCT'].isin([
                'COMMERCIAL.MORTGAGE.CONST', 'MOTORCYCLE.LOAN', 'INVESTMENT.LOAN.BK',
                'ERF.HOTEL.REFINANCING', 'BUSINESS.USED.VEHICLE', 'COMMERCIAL.MORTGAGE.REFINANCE',
                'BUSINESS.NEW.VEHICLE', 'EQUIPMENT.LOAN', 'MEDIUM.TERM.LOAN',
                'COMMERCIAL.MORTGAGE.PURCHASE'
            ])),

            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'MORTGAGE.LOAN') & 
            (self.df['PRODUCT'].isin([
                'RESIDENTIAL.MORT.LOAN.CONST', 'RESIDENTIAL.MORT.LOAN.DIASPORA', 
                'RESIDENTIAL.MORT.HOME.EQUITY', 'RESIDENTIAL.MORTG.LOAN.RENOVTN',
                'RESIDENTIAL.MORT.LOAN.PURCHASE'
            ])),

            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'MORTGAGE.LOAN') & 
            (self.df['PRODUCT'].isin([
                'STAFF.MORT.HOME.PURCHASE', 'STAFF.MORT.HOME.CONSTRUCTN', 
                'STAFF.MORTGAGE.RENOVTN'
            ])),

            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'OTHER.LOANS') & 
            (self.df['PRODUCT_GROUP'] == 'SYNDICATED.LOAN'),

            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'RESTRUCTURING.LOAN') & 
            (self.df['PRODUCT'] == 'RESTRUCTURING.LOAN'),

            (self.df['PRODUCT_LINE'] == 'LENDING') & 
            (self.df['PRODUCT_GROUP'] == 'TREASURY.LOAN') & 
            (self.df['PRODUCT'].isin([
                'CONTRACT.FACILITY', 'TIME.LOAN', 'ZAMUKA.MUGORE', 'ERF.WORKING.CAPITAL',
                'POST.EXPORT.FACILITY', 'AGRICULTURE.INVENTORY.CRED.FIN', 'AGRICULTURAL',
                'INVOICE.DISC.FACILITY', 'UNSE.STOCK.LOAN', 'FACTORING.FACILITY',
                'STOCK.LOAN', 'POST.IMPORT.FACILITY', 'SMALL.ENTERPRISE.LOAN'
            ]))
        ]

        values = [
            'OTHLON',  
            'CONLON',  
            'STLON',   
            'EQULON',  
            'MORLON',  
            'STLON',   
            'OTHLON',  
            'OTHLON',  
            'TRSLON'  
        ]

        self.df['DEAL_TYPE'] = np.select(conditions, values, default='')
        return self

    def map_vision_SBU(self):
    
        conditions = [
            self.df['LEGAL_DOC_NAME'].isin(['NGO', 'NPO']),
            self.df['LEGAL_DOC_NAME'].isin(['ASSOCIATION', 'COOPERATIVE', 'REFERENCE.LETTER', 'IBIMINA']),
            self.df['LEGAL_DOC_NAME'].isin(['EMBASSY']),
            self.df['LEGAL_DOC_NAME'].isin(['NATIONAL.ID', 'NATIONAL.ID.FOR', 'PASSPORT', 'GUARDIAN', 
                                    'EAC.ID', 'GUARDIAN.ID', 'CEPGL.ID', 'NATIONAL.ID.REF', 'CHILD.ID']),
            self.df['SUB_SEG'].isin(['40', '41', '42', '43', '22', '23', '50', '51', '52', '53']),
            self.df['SUB_SEG'].isin(['20']),
            self.df['SUB_SEG'].isin(['21', '25', '30']),
            self.df['SUB_SEG'].isin(['24']),
            self.df['SEGMENT'] == '1'
        ]

        categories = ['NGO', 'SAGRP', 'OTHER', 'RETL', 'LRGOTHR', 'MCEOTHR', 'MEDOTHR', 'SMLOTHR', 'RETL']
        self.df['VISION_SBU'] = np.select(conditions, categories, default='NA')

        return self

    def map_deal_sub_type(self):
        conditions = [
        (self.df['Deal_Type'] == 'TRSLON') & (self.df['Contract_length'] <= 365),
        (self.df['Deal_Type'] == 'TRSLON') & (self.df['Contract_length'] > 365) & (self.df['Contract_length'] <= 5 * 365),
        (self.df['Deal_Type'] == 'TRSLON') & (self.df['Contract_length'] > 5 * 365),
        (self.df['Deal_Type'] == 'MORLON') & (self.df['Contract_length'] <= 365),
        (self.df['Deal_Type'] == 'MORLON') & (self.df['Contract_length'] > 365) & (self.df['Contract_length'] <= 5 * 365),
        (self.df['Deal_Type'] == 'MORLON') & (self.df['Contract_length'] > 5 * 365),
        (self.df['Deal_Type'] == 'TEMDEP') & (self.df['Contract_length'] <= 365),
        (self.df['Deal_Type'] == 'TEMDEP') & (self.df['Contract_length'] > 365) & (self.df['Contract_length'] <= 2 * 365),
        (self.df['Deal_Type'] == 'TEMDEP') & (self.df['Contract_length'] > 2 * 365)
        ]

        # Define corresponding values for Deal_Sub_Type
        values = ['SHTLON', 'MEDLON', 'LNGLON', 'SHTLON', 'MEDLON', 'LNGLON', 'SHTDEP', 'MEDDEP', 'LNGDEP']

        # Apply np.select to create the Deal_Sub_Type column
        self.df['DEAL_SUB_TYPE'] = np.select(conditions, values, default='')
        return self

    def get_mapped_dataframe(self):
        return self.df