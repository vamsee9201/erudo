import streamlit as st
import json
import os

"""
{"users":{"user_id":"a","name":"b","email":""},
"orders":{"order_id":"","user_id":"","amount":"","order_date":"","product":""}
}

"""

def get_db_description(tables_data):
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

with open('openai_key.json', 'r') as file:
    data = json.load(file)
os.environ['OPENAI_API_KEY'] = data["api_key"]

from typing_extensions import TypedDict
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


from typing_extensions import Annotated

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

explanation_text = ""


from langchain.chat_models import init_chat_model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

def write_query(state: State):
    """Generate SQL query to fetch information."""
    # Updated prompt to include explanation text and database details
    prompt = (
        f"Please write a PostgreSQL query based on the following question: '{state['question']}'. "
        f"Ensure that the query does not include any DML statements. "
        f"Here is the structure of the tables and their columns:\n\n{explanation_text}"
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}



# Now , we need to use the text to good use and get the answer from the database.
