
# %%
import psycopg2
db_name = "user_orders"
db_user = "postgres"
db_password = "mysecretpassword"
db_host = "localhost"  # or your database host
db_port = "5433"

conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
cur = conn.cursor()
#%%
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
""")
tables = cur.fetchall()
for table in tables:
    print(table[0])
#%%
for record in cur:
    print(record)
#%%
# ... existing code ...
import json  # Import json module to format the output

def get_tables_and_columns(db_name, db_user, db_password, db_host, db_port):
    # Connect to the specified database
    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    cur = conn.cursor()
    
    # Query to get all tables in the specified database
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    
    result = {}
    
    # Loop through each table to get its columns
    for table in tables:
        table_name = table[0]
        result[table_name] = []  # Initialize a list for columns
        
        # Query to get columns for the current table
        cur.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
        """)
        columns = cur.fetchall()
        
        for column in columns:
            result[table_name].append(column[0])  # Append column name to the list
    
    cur.close()
    conn.close()
    
    return json.dumps(result, indent=4)  # Return the result as a JSON string

# Example usage
db_name = "user_orders"
db_user = "postgres"
db_password = "mysecretpassword"
db_host = "localhost"
db_port = "5433"

print(get_tables_and_columns(db_name, db_user, db_password, db_host, db_port))
# ... existing code ..
# %%
