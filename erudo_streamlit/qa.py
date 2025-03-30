import streamlit as st

"""
{"users":{"user_id":"a","name":"b","email":""},
"orders":{"order_id":"","user_id":"","amount":"","order_date":"","product":""}
}

"""

def qa_functionality(tables_data):
    st.header("Ask a Question")
    question = st.text_input("Type your question here:")
    
    explanation_text = ""
    if st.button("Get Answer"):
        # Combine the question with the input values
        explanation_text = "Here is the structure of the tables and their columns:\n\n"
        for table, columns in tables_data.items():
            explanation_text += f"**Table: {table}**\n"
            for column, description in columns.items():
                explanation_text += f"- **Column:** {column} \n  **Description:** {description}\n"
            explanation_text += "\n"  # Add a newline for better separation between tables
        
        # Display the explanation text
    
        # print("----Tables Data----")
    return explanation_text   # st.write(tables_data) 



# Now , we need to use the text to good use and get the answer from the database.
