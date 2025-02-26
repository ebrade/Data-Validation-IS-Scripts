import oracledb
import os
import time
import xmltodict
import re
import html
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class DBConnector:
    def __init__(self, oracle_query=None):
        self.oracle_query = oracle_query

    def _get_oracle_connection(self):
        """Establishes and returns an Oracle DB connection."""
        return oracledb.connect(
            user=os.environ.get("ORACLE_USER"),
            password=os.environ.get("ORACLE_PASSWORD"),
            host=os.environ.get("ORACLE_HOST"),
            service_name=os.environ.get("ORACLE_NAME")
        )

    def fetch_oracle_data(self):
        """Fetches data based on the provided Oracle query."""
        connection = self._get_oracle_connection()
        cursor = connection.cursor()
        start_t = time.time()

        cursor.execute(self.oracle_query)
        result = cursor.fetchall()
        column_names = [col[0] for col in cursor.description]
        
        print(f"Finished fetching Oracle data in {time.time() - start_t:.2f} secs.")
        cursor.close()
        connection.close()
        
        return {"cols": column_names, "data": result}
    
    def fetch_oracle_data_in_batches(self, recid_prefix_list, query):
        """
        Fetches data based on the provided Oracle query in batches.
        """
        connection = self._get_oracle_connection()
        cursor = connection.cursor()
        all_results = []
        column_names = []
        batch_size = 400  # Ensuring a maximum of 400 parameters
        prefix_batches = [recid_prefix_list[i:i + batch_size] for i in range(0, len(recid_prefix_list), batch_size)]

        for batch in prefix_batches:
            if not batch:
                continue

            # Prepare parameters
            params = {f'p{i}': prefix for i, prefix in enumerate(batch)}
            where_clause = " OR ".join([f"RECID LIKE :p{i} || '%'" for i in range(len(batch))])

            # Replace placeholder in query safely
            batch_query = query.replace("{where_clause}", where_clause)

            # Execute query
            cursor.execute(batch_query, params)
            column_names = [col[0] for col in cursor.description]
            all_results.extend(cursor.fetchall())

        # Close connections
        cursor.close()
        connection.close()

        return {"cols": column_names, "data": all_results}
    
    def fetch_single_record(self):
        """Fetches data based on the provided Oracle query."""
        connection = self._get_oracle_connection()
        cursor = connection.cursor()
        cursor.execute(self.oracle_query)
        result = cursor.fetchone()
        column_names = [col[0] for col in cursor.description]
        cursor.close()
        connection.close()
        
        return {"cols": column_names, "data": [list(result)]}
    
    def fetch_all_tables_oracle(self):
        """Retrieves all table names owned by 'T24'."""
        query = "SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = 'T24'"
        return self._execute_query(query, fetch_column=True)
    
    def count_oracle_tables(self, table_list):
        """Counts the number of records in the given list of tables."""
        connection = self._get_oracle_connection()
        cursor = connection.cursor()
        start_t = time.time()

        result = []
        skipped_tables = []

        for table in table_list:
            query = f"SELECT COUNT(*) FROM T24.{table}"
            try:
                cursor.execute(query)
                result.append({"Tablename": table, "NumOfRecs": cursor.fetchone()[0]})
            except oracledb.DatabaseError as e:
                if "ORA-00942: table or view does not exist" in str(e):
                    skipped_tables.append(table)
                else:
                    raise

        cursor.close()
        connection.close()
        print(f"Counted records for {len(result)} tables in {time.time() - start_t:.2f} secs.")
        print("Skipped Tables:", skipped_tables)
        return result
    
    def fetch_oracle_multi_value(self):
        """Fetches data and processes multi-value XML fields."""
        connection = self._get_oracle_connection()
        cursor = connection.cursor()
        start_t = time.time()

        cursor.execute(self.oracle_query)
        column_names = [col[0] for col in cursor.description]
        result = []

        for records in cursor:
            processed_record = [self._extract_multi_value_field(field) for field in records]
            result.append(processed_record)

        print(f"Finished fetching Oracle data in {time.time() - start_t:.2f} secs.")
        cursor.close()
        connection.close()
        return {'data': result, 'cols': column_names}

    def extract_field(self, field):
        """Extracts values from a field with specific XML patterns."""
        pattern = r"<c(\d+)(?: m=\"(\d+)\")?(?:/|>([^<]*)</c\1>)?"
        matches = re.findall(pattern, field)
        return [{"Value": m[2], "m": m[1]} if m[2] else {"m": m[1]} if m[1] else {} for m in matches]
    
    def to_int(self, val):
        """Converts a value to an integer, returns 0 on failure."""
        try:
            return int(val)
        except ValueError:
            return 0

    def _execute_query(self, query, fetch_column=False):
        """Helper method to execute a query and fetch results."""
        connection = self._get_oracle_connection()
        cursor = connection.cursor()
        start_t = time.time()
        cursor.execute(query)

        result = [row[0] for row in cursor.fetchall()] if fetch_column else cursor.fetchall()

        print(f"Query executed in {time.time() - start_t:.2f} secs.")
        cursor.close()
        connection.close()
        return result

    def _extract_multi_value_field(self, field):
        """Processes fields containing multi-value XML data."""
        if not field or "<c" not in field:
            return field
        pattern = r"<c\d+.*?>([^<]+)</c\d+>"
        return "~".join(html.unescape(match) for match in re.findall(pattern, field))
    def get_common_fields(self, list1, list2):
        return list(set(list1) & set(list2))
    def get_missing_fields(self, main_list, list1):
        return list(set(main_list) - set(list1))
    def get_fields_values(self, cursor, row, columns):
        """
        Retrieve values for a list of column names from a fetchone() result.
        
        :param cursor: The database cursor with a valid description.
        :param row: The fetchone() result (a tuple).
        :param columns: List of column names to extract values for.
        :return: Dictionary {column_name: value} for requested columns.
        """
        if row is None:
            return {}  # Return empty dict if no data
        
        column_names = [desc[0] for desc in cursor.description]  # Extract column names
        row_dict = dict(zip(column_names, row))  # Convert tuple to dictionary
        
        return {col: row_dict.get(col) for col in columns if col in row_dict}  # Filter only requested columns
    def get_COB_Date(self):
        qry = "SELECT LAST_WORKING_DAY FROM T24.V_F_DATES where RECID='RW0010001'"
        oracle_config = {
            "user": os.environ.get("ORACLE_USER"),
            "password": os.environ.get("ORACLE_PASSWORD"),
            "host": os.environ.get("ORACLE_HOST"),
            "service_name": os.environ.get("ORACLE_NAME")
        }
        connection = oracledb.connect(**oracle_config)
        cursor = connection.cursor()
        cursor.execute(qry)
        self.COB_date = cursor.fetchone()[0]
        self.COB_date = datetime.strptime( self.COB_date,"%Y%m%d")

        print(f"COB DATE {self.COB_date}")
        cursor.close()
        connection.close()
       
        return self.COB_date
    @staticmethod
    def check_has_val_with_nodate(data):
        result = {
            "latest": {},
            "has_val_with_nodate": False,
            "keys_with_no_date": []
        }

        # Define a regex to identify dates in the format YYYYMMDD
        date_pattern = re.compile(r'\d{8}$')
        
        # Separate values by their prefixes
        categorized = {}
        for key, value in data.items():
            match = date_pattern.search(value)
            prefix = value.split('-')[0] if '-' in value else None
            
            # Check if the value has a date
            if match:
                date = match.group()
                if prefix:
                    if prefix not in categorized:
                        categorized[prefix] = []
                    categorized[prefix].append((key, value, datetime.strptime(date, "%Y%m%d")))
            else:
                result["has_val_with_nodate"] = True
                result["keys_with_no_date"].append(key)
        
        # Find the oldest entry for each category
        for category, items in categorized.items():
            oldest_item = max(items, key=lambda x: x[2])  # Sort by datetime
            result["latest"][category] = {
                "key": oldest_item[0],
                "value": oldest_item[1],
                "date": oldest_item[2].strftime("%Y-%m-%d")
            }

        return result
    
    def get_multi_value_data(self, multi_var_data, single_var_data, cob_date):
        expanded_data = {}
        
        for col, data in multi_var_data.items():
            expanded_col_data = self.extract_field(data)
            expanded_data[col] = {item.get('m', ''): item.get('Value', None) for item in expanded_col_data}
        if not expanded_data.get("TYPE_SYSDATE", None):
            return []
        check_result = self.check_has_val_with_nodate(expanded_data.get("TYPE_SYSDATE", None))
        
        # getting unique m values
        m_values = set()
        for values in expanded_data.values():
            m_values.update(values.keys())
            
        # Getting all row values
        rows = {}
        for m in m_values:
            row = {key: values.get(m) for key, values in expanded_data.items()}
            row.update(single_var_data)
            rows[m] = row
        
        result = []
        if check_result["has_val_with_nodate"]:
            for key in check_result["keys_with_no_date"]:
                result.append(rows.get(key))
        
        print(result)

    def fetch_ecb(self, multi_var_fields:list):
        cob_date = self.get_COB_Date()
        print(cob_date)
        """Fetch EB Contract Balances"""
        connection = self._get_oracle_connection()
        cursor = connection.cursor()
        cursor.execute(self.oracle_query)
        column_names = [col[0] for col in cursor.description]
        multi_var_fields = self.get_common_fields(column_names, multi_var_fields)
        single_var_fields = self.get_missing_fields(column_names, multi_var_fields)
        
        result = []

        for row in cursor:
            s_fields_data = self.get_fields_values(cursor, row,single_var_fields)
            m_fields_data = self.get_fields_values(cursor, row, multi_var_fields)
            expanded_data = self.get_multi_value_data(m_fields_data, s_fields_data, cob_date)
            result.append(expanded_data)
        return result
