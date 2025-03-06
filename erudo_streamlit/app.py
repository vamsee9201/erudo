import streamlit as st
import json
from qa import qa_functionality  # Import the Q&A functionality

# Title of the app
st.title("Basic Streamlit App")

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

# Initialize input values in session state if not already done
if 'input_values' not in st.session_state:
    st.session_state.input_values = {}

# Initialize json_payload in session state if not already done
if 'json_payload' not in st.session_state:
    st.session_state.json_payload = {"tables": []}  # Default to empty payload

# Sidebar for navigation
tab = st.sidebar.selectbox("Select a tab", ["Admin", "Q&A"])

if tab == "Admin":
    # Text box for entering a link
    link = st.text_input("Enter a link to fetch JSON payload:")
    
    # Button to fetch tables
    if st.button("Fetch Tables"):
        if link:
            st.session_state.json_payload = fetch_json_payload(link)  # Store fetched payload in session state

    # Use the json_payload from session state
    json_payload = st.session_state.json_payload

    # Existing admin functionality
    for table in json_payload["tables"]:
        st.subheader(table["table_name"])  # Display table name as a subheader
        for column in table["columns"]:
            # Use session state to store input values with unique keys
            input_key = f"{table['table_name']}_{column}"  # Create a unique key for each input
            st.session_state.input_values[input_key] = st.text_input(f"{table['table_name']} - {column}", 
                                                                        value=st.session_state.input_values.get(input_key, ""))  # Text input for each column

elif tab == "Q&A":
    qa_functionality(st.session_state.input_values)  # Pass input_values to the Q&A functionality

# ... existing code ...