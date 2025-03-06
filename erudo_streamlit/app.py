import streamlit as st
import json
from qa import qa_functionality  # Import the Q&A functionality

# Title of the app
st.title("Basic Streamlit App")

# Initialize JSON payload
json_payload = {
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

# Toggle sidebar visibility
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True

# Sidebar toggle button
if st.button("Toggle Sidebar"):
    st.session_state.sidebar_visible = not st.session_state.sidebar_visible

# Display sidebar if visible
if st.session_state.sidebar_visible:
    tab = st.sidebar.selectbox("Select a tab", ["Admin", "Q&A"])
else:
    tab = st.selectbox("Select a tab", ["Admin", "Q&A"])  # Main area for tab selection

if tab == "Admin":
    # Existing admin functionality
    for table in json_payload["tables"]:
        st.subheader(table["table_name"])  # Display table name as a subheader
        for column in table["columns"]:
            # Use session state to store input values
            st.session_state.input_values[column] = st.text_input(f"{table['table_name']} - {column}", 
                                                                    value=st.session_state.input_values.get(column, ""))  # Text input for each column

elif tab == "Q&A":
    qa_functionality(st.session_state.input_values)  # Pass input_values to the Q&A functionality

# ... existing code ...