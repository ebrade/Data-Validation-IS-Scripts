import pandas as pd
import re


class DFGenerator(object):
    def __init__(self, filename, file_type='Excel'):
        self.filename = filename
        self.file_type = file_type
        self.df = None

    def read_file(self):
        if self.file_type.lower() == 'excel':
            self.df = pd.read_excel(self.filename, dtype=str)
        elif self.file_type.lower() == 'csv':
            self.df = pd.read_csv(self.filename, dtype=str)
        else:
            raise Exception('File Type Not Supported')

    def change_field_type(self, column_name, new_field_typype='str'):
        self.df[column_name] = self.df[column_name].astype(new_field_typype)

    def fill_zeros(self, col_name, num_of_zeros):
        self.change_field_type(col_name)
        self.df[col_name] = self.df[col_name].str.zfill(num_of_zeros)

    def read_special_csv(self, columns=None, seperator=','):
        if columns:
            return pd.read_csv(self.filename, delimiter=seperator, names=columns, dtype=str, on_bad_lines='warn', engine='python')
        else:
            return pd.read_csv(self.filename, delimiter=seperator, dtype=str, on_bad_lines='warn',engine='python')

    def without_keys(self, d, keys):
        return {x: d[x] for x in d if x not in keys}

    def columnSeperator(self, headercol, valcol):
        list_of_dict = []

        for i, row in self.df.iterrows():
            headers = re.split('!!|::', str(row[headercol]))
            vals = re.split('!!|::', str(row[valcol]))
            dict_data = {}
            for i, h in enumerate(headers):
                if h in dict_data:
                    h = str(h) + "_1"
                    dict_data[h] = vals[i]
                else:
                    dict_data[h] = vals[i]
                    
            shor_row = self.without_keys(dict(row), {"X", "Y"})
            #dict_data = dict(zip(headers, vals))
            shor_row.update(dict_data)
            list_of_dict.append(shor_row)

        self.df = pd.DataFrame(list_of_dict)

    def read_and_clean(self, columns, headercol, valcol):
        self.read_special_csv(columns=columns)
        self.columnSeperator(headercol=headercol, valcol=valcol)
