import streamlit as st
import json
from qa import qa_functionality 
import psycopg2
 # Import the Q&A functionality

# Function to load user credentials from a JSON file
def load_user_credentials():
    with open('users.json') as f:
        data = json.load(f)
    return data['users']

# Function to simulate fetching JSON payload based on a link
def fetch_json_payload(link):
    # For demonstration, we return the same JSON payload regardless of the link
    return {
        "tables": [
            {
                "table_name": "table_1",
                "columns": ["column_1", "column_2"]
            },
            {
                "table_name": "table_2",
                "columns": ["column_1", "column_2", "column_3"]
            },
            {
                "table_name": "table_3",
                "columns": ["column_1"]
            },
            {
                "table_name": "table_4",
                "columns": ["column_1", "column_2", "column_3", "column_4"]
            },
            {
                "table_name": "table_5",
                "columns": []
            }
        ]
    }

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
    
    return result

# Initialize input values in session state if not already done

#db_name = "user_orders"
db_user = "postgres"
db_password = "mysecretpassword"
db_host = "localhost"
db_port = "5433"

if 'tables_data' not in st.session_state:
    st.session_state.tables_data = {}

# Initialize json_payload in session state if not already done
if 'json_payload' not in st.session_state:
    st.session_state.json_payload = {}  # Default to empty payload

# Sidebar for navigation
tab = st.sidebar.selectbox("Select a tab", ["Admin", "Q&A"])

if tab == "Admin":
    # Text box for entering a link
    db_name = st.text_input("Enter a database name to fetch tables and columns:")
    
    # Button to fetch tables
    if st.button("Fetch Tables"):
        if db_name:
            st.session_state.json_payload = get_tables_and_columns(db_name, db_user, db_password, db_host, db_port)  # Store fetched payload in session state

    # Use the json_payload from session state
    json_payload = st.session_state.json_payload

    # Existing admin functionality
    tables_data = st.session_state.tables_data
    for table_name, columns in st.session_state.json_payload.items():
        st.subheader(table_name)
        
        # Initialize the dictionary for this table if it doesn't exist
        if table_name not in tables_data:
            tables_data[table_name] = {}

        for column in columns:
            # Pre-fill value from tables_data if it exists, otherwise use ""
            column_description = st.text_input(
                f"{table_name} - {column} Description", 
                value=tables_data[table_name].get(column, "")
            )
            
            # Save it back into tables_data
            tables_data[table_name][column] = column_description

    # Store the structured data in session state
    st.session_state.tables_data = tables_data # Text input for each column

elif tab == "Q&A":
    qa_functionality(st.session_state.tables_data)  # Pass input_values to the Q&A functionality

# ... existing code ...