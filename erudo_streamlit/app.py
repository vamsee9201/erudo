import streamlit as st
import json

# Title of the app
st.title("Basic Streamlit App")

# Initialize JSON payload
json_payload = {
    "tables": ["table_1", "table_2", "table_3", "table_4", "table_5"]
}

# Create a dictionary to hold the input values
input_values = {}

# Create text inputs for each table name
for table_name in json_payload["tables"]:
    input_values[table_name] = st.text_input(table_name)

# Function to concatenate input values
def concatenate_inputs(inputs):
    return " ".join(inputs.values())

# Dummy button to process inputs
if st.button("Concatenate Inputs"):
    result = concatenate_inputs(input_values)
    st.write("Concatenated Result:")
    st.write(result)  # Display the concatenated result
