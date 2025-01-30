import pynuodb
import oracledb
import pandas as pd
import os
import time
import asyncio
import xmltodict
import jaydebeapi
import jpype.imports
import jpype
from concurrent.futures import ThreadPoolExecutor
import re
import html
from dotenv import load_dotenv
import os
load_dotenv() 


# ORACLE_HOST=dc1r01uat-scan
class DBConnector():
    def __init__(self, nuodb_query=None, oracle_query=None) -> None:
            self.nuodb_query = nuodb_query
            self.oracle_query = oracle_query
    async def fetch_nuodb_data(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        options = {"schema": NUODB_SCHEMA, 'direct':'true'}
        
        connect_kw_args = {'database': NUODB_NAME, 'host':NUODB_HOST, 
                        'user': NUODB_USER, 'password':NUODB_PASSWORD, 'options': options}
        
        connection = pynuodb.connect(**connect_kw_args)
        cursor =  connection.cursor()
        # cursor.arraysize = 1000
        # cursor.prefetchrows = 2000 
        
        cursor.execute(self.nuodb_query)
        column_names = [item[0] for item in cursor.description]
        result = []
        while True:
                row = cursor.fetchone()
                if not row:
                        break
                result.append(row)
        cursor.close()
        connection.close()
        print("Finished fetching Nuodb .... in %s secs....."% (time.time() - start_t))
        return {"cols": column_names, "data": result}

    async def fetch_oracle_data(self):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection =  oracledb.connect(user=ORACLE_USER,
                                      password=ORACLE_PASSWORD,
                                      host=ORACLE_HOST,
                                      service_name=ORACLE_NAME)
        cursor =  connection.cursor()
        # cursor.arraysize = 250
        # cursor.prefetchrows = 2000 
        start_t = time.time()
        cursor.execute(self.oracle_query)
        result = []
        while True:
                row = cursor.fetchone()
                if not row:
                        break
                result.append(row)
        # result = cursor.fetchall()
        column_names = [item[0] for item in cursor.description]
        print("Finished fetching Oracle .... in %s secs....."% (time.time() - start_t))
        cursor.close()
        connection.close()
        return {"cols": column_names, "data": result}
        
    def fetch_oracle_data_sync_mode(self):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection =  oracledb.connect(user=ORACLE_USER,
                                      password=ORACLE_PASSWORD,
                                      host=ORACLE_HOST,
                                      service_name=ORACLE_NAME)
        cursor =  connection.cursor()
        # cursor.arraysize = 1000  
        # cursor.prefetchrows = 2000 
        start_t = time.time()
        cursor.execute(self.oracle_query)
        result = []
        while True:
                row = cursor.fetchone()
                if not row:
                        break
                result.append(row)
        column_names = [item[0] for item in cursor.description]
        print("Finished fetching Oracle .... in %s secs....."% (time.time() - start_t))
        cursor.close()
        connection.close()
        return {"cols": column_names, "data": result}
    def fetch_nuodb_data_sync_mode(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("nuodb", NUODB_SCHEMA)
        options = {"schema": NUODB_SCHEMA}
        connect_kw_args = {'database': NUODB_NAME, 'host':NUODB_HOST, 
                        'user': NUODB_USER, 'password':NUODB_PASSWORD, 'options': options}
        connection = pynuodb.connect(**connect_kw_args)
        cursor =  connection.cursor()
        cursor.arraysize = 250
        # cursor.prefetchrows = 2000 
        start_t = time.time()
        cursor.execute(self.nuodb_query)
        column_names = [item[0] for item in cursor.description]
        result = []
        while True:
                row = cursor.fetchone()
                if not row:
                        break
                result.append(row)
        cursor.close()
        connection.close()
        print("Finished fetching Nuodb .... in %s secs....."% (time.time() - start_t))
        return {"cols": column_names, "data": result}
    
    def fetch_all_tables_oracle(self):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection =  oracledb.connect(user=ORACLE_USER,
                                      password=ORACLE_PASSWORD,
                                      host=ORACLE_HOST,
                                      service_name=ORACLE_NAME)
        cursor =  connection.cursor() 
        start_t = time.time()
        query = """
        SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER= 'T24'
        """
        cursor.execute(query)
        result = []
        while True:
                row = cursor.fetchone()
                if not row:
                    break                
                result.append(row[0])
        cursor.close()
        connection.close()
        print("Finished Counting Oracle tables .... in %s secs....."% (time.time() - start_t))
        return result
    def parse_field(self, field):
        """Helper function to parse a single field."""
        if field and "<" in field and ">" in field:
            f_values = field.split("\n")
            cleaned_field = []
            
            for val in f_values:
                if val.strip():
                    val_clean = xmltodict.parse(val)
                    first_key, first_value = val_clean.popitem()
                    if isinstance(first_value, dict):
                        cleaned_field.append(first_value.get('#text'))
                    else:
                        cleaned_field.append(first_value)
            cleaned_field = ["" if x is None else x for x in cleaned_field]
            return "~".join(cleaned_field)
        else:
            return field
    
    def get_all_tables_nuodb(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        
        options = {"schema": NUODB_SCHEMA}
        connect_kw_args = {'database': NUODB_NAME, 'host':NUODB_HOST, 
                        'user': NUODB_USER, 'password':NUODB_PASSWORD, 'options': options}
        connection = pynuodb.connect(**connect_kw_args)
        cursor =  connection.cursor() 
        start_t = time.time()
        query = """
        SELECT TABLENAME
        FROM SYSTEM.TABLES;
        """
        cursor.execute(query)
        result = []
        while True:
                row = cursor.fetchone()
                if not row:
                    break                
                result.append(row[0])
        cursor.close()
        connection.close()
        print("Finished Counting Nuodb tables .... in %s secs....."% (time.time() - start_t))
        return result
    
    def count_oracle_tables(self, table_list=None):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection =  oracledb.connect(user=ORACLE_USER,
                                      password=ORACLE_PASSWORD,
                                      host=ORACLE_HOST,
                                      service_name=ORACLE_NAME) 
        start_t = time.time()
        result = []
        counted_tables = 0

        try:
            cursor = connection.cursor()
            skipped_tables = []

            for table in table_list:
                query = f"SELECT COUNT(*) FROM T24.{table}"
                try:
                    cursor.execute(query)
                    record_count = cursor.fetchone()[0]
                    result.append({"Tablename":table, "NumOfRecs":record_count})
                    counted_tables = counted_tables + 1
                except oracledb.DatabaseError as e:
                    if 'ORA-00942: table or view does not exist' in str(e):
                        skipped_tables.append(table)
                    else:
                        raise  # Re-raise other exceptions for further handling

        except Exception as e:
            print(f"Unexpected error: {e}")  # Handle general exceptions

        finally:
            cursor.close()
            connection.close() # Close the connection after all operations

        elapsed_time = time.time() - start_t
        print(f"Counted records for {counted_tables} tables in {elapsed_time:.2f} seconds.")
        print("---------------- Table Skipped-----------------\n", 
              skipped_tables,
              "\n---------------- Table Skipped-----------------\n")

        return result
    
    def get_all_nuodb_tables(self, table_list=None):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        
        # JDBC connection string
        start_t = time.time()
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            column_names = [item[0] for item in cursor.description]
            result = []
            while True:
                    row = cursor.fetchone()
                    if not row:
                            break
                    result.append(row[0])
            cursor.close()
            connection.close()
            print("Finished fetching Nuodb .... in %s secs....."% (time.time() - start_t))
            return {"cols": column_names, "data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")
    
    
    
   
    def fetch_nuodb_in_jdbc_mode(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        
        # JDBC connection string
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            column_names = [item[0] for item in cursor.description]
            result = []
            while True:
                    row = cursor.fetchone()
                    if not row:
                            break
                    result.append(row)
            cursor.close()
            connection.close()
            print("Finished fetching Nuodb .... in %s secs....."% (time.time() - start_t))
            return {"cols": column_names, "data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")
    
    def fetch_nuodb_in_jdbc_mode_Bills(self, output_file):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        
        # JDBC connection string
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            column_names = [item[0] for item in cursor.description]
            result = []
            with open(output_file, 'w', encoding="utf-8") as out_file:
                column_names = ["RECID", "XMLRECORD"]
                out_file.write("|".join(column_names) + "\n")
                while True:
                        row = cursor.fetchone()
                        if not row:
                                break
                        a = []
                        
                        out_file.write("|".join(row) + "\n")
                        
                cursor.close()
                connection.close()
                print("Finished fetching Nuodb .... in %s secs....."% (time.time() - start_t))
                return {"cols": column_names, "data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")

    def fetch_nuodb_in_jdbc_mode_arr_details(self, output_file):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        
        # JDBC connection string
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            column_names = [item[0] for item in cursor.description]
            result = []
            with open(output_file, 'w', encoding="utf-8") as out_file:
                column_names = ["RECID", "XMLAA", "XMLAAC", "XMLAAB"] 
                out_file.write("|".join(column_names) + "\n")
                while True:
                        row = cursor.fetchone()
                        if not row:
                                break
                        a = []
                        row = [item if item is not None else "" for item in row]
                        
                        out_file.write("|".join(row) + "\n")
                        
                cursor.close()
                connection.close()
                print("Finished fetching Nuodb .... in %s secs....."% (time.time() - start_t))
                return {"cols": column_names, "data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")  


    def fetch_oracle_multi_value(self):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection = oracledb.connect(user=ORACLE_USER,
                                    password=ORACLE_PASSWORD,
                                    host=ORACLE_HOST,
                                    service_name=ORACLE_NAME)
        cursor = connection.cursor()
        
        start_t = time.time()
        cursor.execute(self.oracle_query)
        column_names = [item[0] for item in cursor.description]
        result = []

        
        while True:
            records = cursor.fetchone()  # Fetch records in batches
            if not records:
                break

            fine_tuned_record = []

            for field in records:
                # Define the regular expression pattern to match the desired values
                pattern = r'<c\d+.*?>([^<]+)</c\d+>'

                if field is None:
                    fine_tuned_record.append(field)   
                    continue  
                elif "<c" not in field and not "</c" in field:
                    fine_tuned_record.append(field)   
                    continue   
                # Find all matches in the input text
                matches = re.findall(pattern, field)
                
                # Decode HTML entities in each match
                decoded_matches = [html.unescape(match) for match in matches]
                
                # Join the decoded matches with a '~' separator
                rec_fine = '~'.join(decoded_matches)
                fine_tuned_record.append(rec_fine)
                
            
            result.append(fine_tuned_record)
        
        print("Finished fetching Oracle .... in %.2f secs....." % (time.time() - start_t))
        cursor.close()
        connection.close()
        return {'data': result, 'cols': column_names}
    
    def fetch_nuodb_multi_value(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        
        # JDBC connection string
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            column_names = [item[0] for item in cursor.description]
            result = []
            special_chars = ["\uf8fd", ""]
            while True:
                    row = cursor.fetchone()
                    special_chars_pattern = re.compile(r"[\uf8fd]+")
                    cleaned_rec = []
                    if not row:
                            break
                    for field in row:
                        if field and special_chars_pattern.search(field):
                            # Replace special characters with a tilde, strip leading/trailing spaces, and split by tildes
                            f_val = re.sub(special_chars_pattern, "~", field).strip()
                            # Split by tilde and filter out empty parts, then join again with a single tilde
                            f_val = "~".join(part for part in f_val.split("~") if part)
                            cleaned_rec.append(f_val)
                        else:
                            cleaned_rec.append(field)
                    result.append(cleaned_rec)
            cursor.close()
            connection.close()
            print("Finished fetching Nuodb .... in %.2f secs....."% (time.time() - start_t))
            return {"cols": column_names, "data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")
    
    def extract_field(self, field):
        pattern = r"<c(\d+)(?: m=\"(\d+)\")?(?:/|>([^<]*)</c\1>)?"

        # Find all matches
        matches = re.findall(pattern, field)

        # Extract data and build dictionaries
        data = []
        for match in matches:
            if match[2]:  # Check if there's a value in the third group
                entry = {
                    'Value': match[2],
                    'm': match[1]
                }
            elif match[1]:  # Check if the m attribute is present
                entry = {
                    'm': match[1]
                }
            else:
                entry = {}
            data.append(entry)
        return data
    
    def to_int(self, val):
         try:
            return float(val)
         except:
              return 0
    
    def expand_multivalue_fields(self,row):
        # Extract multi-value fields
        currencies = row['CURRENCY']
        balances = row['BALANCE']
        ccy_balances = row['CCY_BALANCE']
        debit_movements = row['DEBIT_MOVEMENT']
        credit_movements = row['CREDIT_MOVEMENT']
        balance_ytds = row['BALANCE_YTD']
        ccy_balance_ytds = row['CCY_BALANCE_YTD']
        APPLIC_ID_s= row['APPLIC_ID']
        DATE_LAST_UPDATE_s= row['DATE_LAST_UPDATE']
        PLCATEGORY_s= row['PLCATEGORY']
        PLPRODUCT_s= row['PLPRODUCT']
        PLSECTOR_s= row['PLSECTOR']
        PLDEPARTMENT_s= row['PLDEPARTMENT']
        PLRESIDENCE_s= row['PLRESIDENCE']
        PLBOOK_s= row['PLBOOK']
        PLSTATUS_s= row['PLSTATUS']
        PLSTATUS_s= row['PLSTATUS']
        
        max_length = max(len(currencies), len(balances), len(ccy_balances), len(debit_movements), len(credit_movements), len(balance_ytds), len(ccy_balance_ytds))
        
        new_rows = []
        for i in range(max_length):
            new_row = row.copy()
            new_row['APPLIC_ID'] = APPLIC_ID_s[0]["Value"] if APPLIC_ID_s else ''
            new_row['DATE_LAST_UPDATE'] = DATE_LAST_UPDATE_s[0]["Value"] if DATE_LAST_UPDATE_s else ''
            new_row['PLCATEGORY'] = PLCATEGORY_s[0]["Value"] if PLCATEGORY_s else ''
            new_row['PLPRODUCT'] = PLPRODUCT_s[0]["Value"] if PLPRODUCT_s else ''
            new_row['PLSECTOR'] = PLSECTOR_s[0]["Value"] if PLSECTOR_s else ''
            new_row['PLDEPARTMENT'] = PLDEPARTMENT_s[0]["Value"] if PLDEPARTMENT_s else ''
            new_row['PLRESIDENCE'] = PLRESIDENCE_s[0]["Value"] if PLRESIDENCE_s else ''
            new_row['PLBOOK'] = PLBOOK_s[0]["Value"] if PLBOOK_s else ''
            new_row['PLSTATUS'] =  PLSTATUS_s[0]["Value"] if PLSTATUS_s else ''
            new_row['PLSTATUS'] = PLSTATUS_s[0]["Value"] if PLSTATUS_s else ''
            new_row['CURRENCY'] = currencies[i]['Value'] if i < len(currencies) and 'Value' in currencies[i]  else ''
            new_row['BALANCE'] = balances[i]['Value'] if i < len(balances) and 'Value' in  balances[i] else ''
            new_row['CCY_BALANCE'] = ccy_balances[i]['Value'] if i < len(ccy_balances) and 'Value' in ccy_balances[i] else ''
            new_row['DEBIT_MOVEMENT'] = debit_movements[i]['Value'] if i < len(debit_movements) and 'Value' in debit_movements[i] else ''
            new_row['CREDIT_MOVEMENT'] = credit_movements[i]['Value'] if i < len(credit_movements) and 'Value' in credit_movements[i] else ''
            new_row['BALANCE_YTD'] = balance_ytds[i]['Value'] if i < len(balance_ytds) and 'Value' in balance_ytds[i] else ''
            new_row['CCY_BALANCE_YTD'] = ccy_balance_ytds[i]['Value'] if i < len(ccy_balance_ytds) and 'Value' in ccy_balance_ytds[i] else ''

            daily_mvt = self.to_int(new_row['DEBIT_MOVEMENT']) + self.to_int(new_row['CREDIT_MOVEMENT'])
            new_row["CLOSING_BALANCE"] = self.to_int(new_row['BALANCE']) + daily_mvt + self.to_int(new_row['BALANCE_YTD'])
            new_row["OPENNING_BALANCE"] = self.to_int(new_row['BALANCE']) + self.to_int(new_row['BALANCE_YTD'])
            new_rows.append(new_row)
        return new_rows
    
    def expand_multivalue_fields_CAL(self,row):
        # Extract multi-value fields
        APPLIC_ID_s = row["APPLIC_ID"]
        CURRENCY_MARKET_s = row["CURRENCY_MARKET"]
        POSITION_TYPE_s = row["POSITION_TYPE"]
        K_CURRENCY_s = row["K_CURRENCY"]
        K_TYPE_s = row["K_TYPE"]
        DATE_LAST_UPDATE_s = row["DATE_LAST_UPDATE"]
        BALANCE_s = row["BALANCE"]
        LOCAL_BALANCE_s = row["LOCAL_BALANCE"]
        DEBIT_MOVEMENT_s = row["DEBIT_MOVEMENT"]
        LOCAL_DEBIT_MVE_s = row["LOCAL_DEBIT_MVE"]
        CREDIT_MOVEMENT_s = row["CREDIT_MOVEMENT"]
        LOCAL_CREDT_MVE_s = row["LOCAL_CREDT_MVE"]
        
        max_length = max(len(APPLIC_ID_s), len(CURRENCY_MARKET_s), len(POSITION_TYPE_s), 
                         len(K_CURRENCY_s), len(DATE_LAST_UPDATE_s), len(BALANCE_s), 
                         len(LOCAL_BALANCE_s), len(DEBIT_MOVEMENT_s), len(LOCAL_DEBIT_MVE_s), 
                         len(CREDIT_MOVEMENT_s), len(LOCAL_CREDT_MVE_s), len(K_TYPE_s)
                         ) 
        new_rows = []
        for i in range(max_length):
            new_row = row.copy()
            new_row['DATE_LAST_UPDATE'] = DATE_LAST_UPDATE_s[0]["Value"] if DATE_LAST_UPDATE_s else ''
            new_row['APPLIC_ID'] = APPLIC_ID_s[0]["Value"] if APPLIC_ID_s else ''
            new_row["CURRENCY_MARKET"] = CURRENCY_MARKET_s[0]["Value"] if CURRENCY_MARKET_s else ''
            new_row["POSITION_TYPE"] = POSITION_TYPE_s[0]["Value"] if POSITION_TYPE_s else ''
            new_row["K_CURRENCY"] = K_CURRENCY_s[0]["Value"] if K_CURRENCY_s else ''
            new_row["K_TYPE"] = K_TYPE_s[i]["Value"] if i < len(K_TYPE_s) and 'Value' in K_TYPE_s[i] else None
            new_row["BALANCE"] = BALANCE_s[i]["Value"] if i < len(BALANCE_s) and 'Value' in BALANCE_s[i] else None
            new_row["LOCAL_BALANCE"] = LOCAL_BALANCE_s[i]["Value"] if i < len(LOCAL_BALANCE_s) and 'Value' in LOCAL_BALANCE_s[i] else None
            new_row["DEBIT_MOVEMENT"] = DEBIT_MOVEMENT_s[i]["Value"] if i < len(DEBIT_MOVEMENT_s) and 'Value' in DEBIT_MOVEMENT_s[i] else None
            new_row["LOCAL_DEBIT_MVE"] = LOCAL_DEBIT_MVE_s[i]["Value"] if i < len(LOCAL_DEBIT_MVE_s) and 'Value' in LOCAL_DEBIT_MVE_s[i] else None
            new_row["CREDIT_MOVEMENT"] = CREDIT_MOVEMENT_s[i]["Value"] if i < len(CREDIT_MOVEMENT_s) and 'Value' in CREDIT_MOVEMENT_s[i] else None
            new_row["LOCAL_CREDT_MVE"] = LOCAL_CREDT_MVE_s[i]["Value"] if i < len(LOCAL_CREDT_MVE_s) and 'Value' in LOCAL_CREDT_MVE_s[i] else None

            if new_row["K_CURRENCY"]=="RWF":
                new_row["LOCAL_BALANCE"] = new_row["BALANCE"]
                new_row["LOCAL_DEBIT_MVE"] = new_row["DEBIT_MOVEMENT"]
                new_row["LOCAL_CREDT_MVE"] = new_row["CREDIT_MOVEMENT"]

            new_row["CLOSING_BALANCE"] = self.to_int(new_row["LOCAL_BALANCE"]) + self.to_int(new_row["LOCAL_DEBIT_MVE"]) + \
                                        self.to_int(new_row["LOCAL_CREDT_MVE"])

            new_rows.append(new_row)
        return new_rows


    def fetch_oracle_CPL(self):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection = oracledb.connect(user=ORACLE_USER,
                                    password=ORACLE_PASSWORD,
                                    host=ORACLE_HOST,
                                    service_name=ORACLE_NAME)
        cursor = connection.cursor()
        
        start_t = time.time()
        cursor.execute(self.oracle_query)
        column_names = [item[0] for item in cursor.description]
        result = []

        
        while True:
            records = cursor.fetchone()  # Fetch records in batches
            if not records:
                break
            all_recs = {}
            
            for id, field in enumerate(records):
                
                if field and "<c" not in field and "/>" not in field:
                    data = field
                elif not field:
                     data = ""
                else:                 
                    data = self.extract_field(field)
                     
                col = column_names[id]
                all_recs[col]=data
            new_rows = self.expand_multivalue_fields(all_recs)
            
            result.extend(new_rows)
        
        print("Finished fetching Oracle .... in %.2f secs....." % (time.time() - start_t))
        cursor.close()
        connection.close()
        return {'data': result}
    


    def fetch_oracle_CAL(self):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection = oracledb.connect(user=ORACLE_USER,
                                    password=ORACLE_PASSWORD,
                                    host=ORACLE_HOST,
                                    service_name=ORACLE_NAME)
        cursor = connection.cursor()
        
        start_t = time.time()
        cursor.execute(self.oracle_query)
        column_names = [item[0] for item in cursor.description]
        result = []

        
        while True:
            records = cursor.fetchone()  # Fetch records in batches
            if not records:
                break
            all_recs = {}
            
            for id, field in enumerate(records):
                
                if field and "<c" not in field and "/>" not in field:
                    data = field
                elif not field:
                     data = ""
                else:                 
                    data = self.extract_field(field)
                     
                col = column_names[id]
                all_recs[col]=data
            new_rows = self.expand_multivalue_fields_CAL(all_recs)            
            result.extend(new_rows)
        
        print("Finished fetching Oracle .... in %.2f secs....." % (time.time() - start_t))
        cursor.close()
        connection.close()
        return {'data': result}
    
    def fetch_nuodb_CAL(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        
        # JDBC connection string
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            column_names = [item[0] for item in cursor.description]
            result = []
            
            while True:
                    row = cursor.fetchone()
                    special_chars_pattern = re.compile(r"[\uf8fd]+")
                    cleaned_rec = {}
                    
                    if not row:
                        break
                    for id, field in enumerate(row):
                        col = column_names[id]
                        
                        if id == 0:                            
                            cleaned_rec[col]=field                            
                        else:
                            data = []
                            if field and special_chars_pattern.search(field):
                                # Replace special characters with a tilde, strip leading/trailing spaces, and split by tildes
                                records = re.split(special_chars_pattern,field.strip())                            
                                
                                for i, val in enumerate(records):
                                    if i==0:
                                        entry = {"Value":val}
                                        
                                    else:
                                        entry = {"Value":val, "m": i+1}
                                    data.append(entry)                           
                            else:
                                entry = {"Value":field}
                                data.append(entry)
                            cleaned_rec[col] = data
                            
                    
                    new_rows = self.expand_multivalue_fields_CAL(row=cleaned_rec)
                    
                    result.extend(new_rows)
            cursor.close()
            connection.close()
            print("Finished fetching Nuodb .... in %.2f secs....."% (time.time() - start_t))
            return {"data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")

    def fetch_nuodb_CPL(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        
        # JDBC connection string
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            column_names = [item[0] for item in cursor.description]
            result = []
            
            while True:
                    row = cursor.fetchone()
                    special_chars_pattern = re.compile(r"[\uf8fd]+")
                    cleaned_rec = {}
                    
                    if not row:
                        break
                    for id, field in enumerate(row):
                        col = column_names[id]
                        
                        if id == 0:                            
                            cleaned_rec[col]=field                            
                        else:
                            data = []
                            if field and special_chars_pattern.search(field):
                                # Replace special characters with a tilde, strip leading/trailing spaces, and split by tildes
                                records = re.split(special_chars_pattern,field.strip())                            
                                
                                for i, val in enumerate(records):
                                    if i==0:
                                        entry = {"Value":val}
                                        
                                    else:
                                        entry = {"Value":val, "m": i+1}
                                    data.append(entry)                           
                            else:
                                entry = {"Value":field}
                                data.append(entry)
                            cleaned_rec[col] = data
                            
                    
                    new_rows = self.expand_multivalue_fields(row=cleaned_rec)
                    
                    result.extend(new_rows)
            cursor.close()
            connection.close()
            print("Finished fetching Nuodb .... in %.2f secs....."% (time.time() - start_t))
            return {"data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")

    def fetch_nuodb_Seq_no(self):
        NUODB_USER = os.environ.get("NUODB_USER", None)
        NUODB_PASSWORD = os.environ.get("NUODB_PASSWORD", None)
        NUODB_HOST = os.environ.get("NUODB_HOST", None)
        NUODB_NAME = os.environ.get("NUODB_NAME", None)
        NUODB_SCHEMA = os.environ.get("NUODB_SCHEMA", None)
        print("Nuodb")
        start_t = time.time()
        
        # JDBC connection string
        jdbc_url = f"jdbc:com.nuodb://{NUODB_HOST}/{NUODB_NAME}?schema={NUODB_SCHEMA}&direct=true"
        driver_class = "com.nuodb.jdbc.Driver"
        jar_file = "./NuoDBJDBC/nuodb-jdbc-24.1.2.jar"

        try:
            connection = jaydebeapi.connect(driver_class, jdbc_url, [NUODB_USER, NUODB_PASSWORD], jar_file)
                    
            # Use the connection
            cursor = connection.cursor()
            cursor.execute(self.nuodb_query)
            
            result = []
            
            while True:
                    row = cursor.fetchone()
                    cleaned_rec = {}
                    if not row:
                            break
                    row_dat = row[0].split("*")
                    cleaned_rec["SEQ_NO"] = row_dat[0]
                    cleaned_rec["CONSOL_KEY"] = row_dat[1]
                    cleaned_rec["K_TYPE"] = row_dat[2]
                    result.append(cleaned_rec)
            cursor.close()
            connection.close()
            print("Finished fetching Nuodb .... in %.2f secs....."% (time.time() - start_t))
            return {"data": result}

        except Exception as e:
            print(f"Error connecting to NuoDB via JDBC: {e}")


    def fetch_oracle_Seq_no(self):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection = oracledb.connect(user=ORACLE_USER,
                                    password=ORACLE_PASSWORD,
                                    host=ORACLE_HOST,
                                    service_name=ORACLE_NAME)
        cursor = connection.cursor()
        
        start_t = time.time()
        cursor.execute(self.oracle_query)
        column_names = [item[0] for item in cursor.description]
        result = []

        
        while True:
            records = cursor.fetchone()  # Fetch records in batches
            if not records:
                break
            cleaned_rec = {}
            row_dat = records[0].split("*")
            cleaned_rec["SEQ_NO"] = row_dat[0]
            cleaned_rec["CONSOL_KEY"] = row_dat[1]
            cleaned_rec["K_TYPE"] = row_dat[2]
            result.append(cleaned_rec)
            
        
        print("Finished fetching Oracle .... in %.2f secs....." % (time.time() - start_t))
        cursor.close()
        connection.close()
        return {'data': result}
    
    def fetch_oracle_accruals(self, output_file):
        ORACLE_USER = os.environ.get("ORACLE_USER", None)
        ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", None)
        ORACLE_HOST = os.environ.get("ORACLE_HOST", None)
        ORACLE_NAME = os.environ.get("ORACLE_NAME", None)
        print("oracle")

        connection = oracledb.connect(user=ORACLE_USER,
                                    password=ORACLE_PASSWORD,
                                    host=ORACLE_HOST,
                                    service_name=ORACLE_NAME)
        cursor = connection.cursor()
        
        start_t = time.time()
        cursor.execute(self.oracle_query)
        column_names = [item[0] for item in cursor.description]
        result = []

        try:
            with open(output_file, 'w', encoding="utf-8") as out_file:
                column_names = ["XMLRECORD"]
                out_file.write("|".join(column_names) + "\n")
                while True:
                        row = cursor.fetchone()
                        if not row:
                                break
                        a = []
                        
                        out_file.write("|".join(row) + "\n")
                        
                cursor.close()
                connection.close()
                print("Finished fetching Nuodb .... in %s secs....."% (time.time() - start_t))
                return {"cols": column_names, "data": result}

        except Exception as e:
            print(f"Error connecting to JDBC via JDBC: {e}")