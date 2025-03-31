import psycopg2
import json
from decimal import Decimal
import datetime

# Load database configuration from a JSON file or define them here
def load_db_config():
    with open('db_config.json') as f:
        return json.load(f)

# Function to connect to the database
def connect_to_db(db_name, db_user, db_password, db_host, db_port):
    return psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

# Function to get all tables and their columns
def get_tables_and_columns(db_name, db_user, db_password, db_host, db_port):
    conn = connect_to_db(db_name, db_user, db_password, db_host, db_port)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    
    result = {}
    
    for table in tables:
        table_name = table[0]
        result[table_name] = []
        
        cur.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
        """)
        columns = cur.fetchall()
        
        for column in columns:
            result[table_name].append(column[0])
    
    cur.close()
    conn.close()
    
    return result

# Function to execute a query and return results as JSON
def get_query_result(db_name, db_user, db_password, db_host, db_port, query):
    conn = connect_to_db(db_name, db_user, db_password, db_host, db_port)
    cur = conn.cursor()
    
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    results = cur.fetchall()
    
    json_results = []
    for row in results:
        json_row = {}
        for col_name, value in zip(columns, row):
            if isinstance(value, Decimal):
                json_row[col_name] = float(value)
            elif isinstance(value, datetime.date):
                json_row[col_name] = value.isoformat()
            else:
                json_row[col_name] = value
        json_results.append(json_row)
    
    cur.close()
    conn.close()
    
    return json.dumps(json_results, indent=4)

# Example usage
# db_config = load_db_config()
# tables = get_tables_and_columns(db_config['db_name'], db_config['db_user'], db_config['db_password'], db_config['db_host'], db_config['db_port'])
# print(tables) 