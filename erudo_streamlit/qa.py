#%%
import streamlit as st
import json
import os
from decimal import Decimal
import datetime
from db import get_query_result  # Import from db.py
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model

"""
{"users":{"user_id":"a","name":"b","email":""},
"orders":{"order_id":"","user_id":"","amount":"","order_date":"","product":""}
}

"""

#%%
# Example usage
db_name = "user_orders"
db_user = "postgres"
db_password = "mysecretpassword"
db_host = "localhost"
db_port = "5433"

def get_db_description(tables_data):
    #st.header("Ask a Question")
    #question = st.text_input("Type your question here:")
    
    explanation_text = "Here is the structure of the tables and their columns:\n\n"
    for table, columns in tables_data.items():
        explanation_text += f"**Table: {table}**\n"
        for column, description in columns.items():
            explanation_text += f"- **Column:** {column} \n  **Description:** {description}\n"
        explanation_text += "\n"  # Add a newline for better separation between tables
    
    return explanation_text   # st.write(tables_data) 

#print(get_db_description(tables_data))
#%%

with open('openai_key.json', 'r') as file:
    data = json.load(file)
os.environ['OPENAI_API_KEY'] = data["api_key"]

from typing_extensions import TypedDict
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    explanation_text: str


from typing_extensions import Annotated

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

#%%

# Initialize the language model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

def write_query(state: State):
    """Generate SQL query to fetch information."""
    # Updated prompt to include explanation text and database details
    prompt = (
        f"Please write a PostgreSQL query based on the following question: '{state['question']}'. "
        f"Ensure that the query does not include any DML statements. "
        f"Here is the structure of the tables and their columns:\n\n{state['explanation_text']}"
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)

    return {"query": result["query"]}

#%%

def execute_query(state: State):
    """Execute SQL query."""
    query_result = get_query_result(db_name, db_user, db_password, db_host, db_port, state["query"])
    return {"result": query_result}

def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}


#%%
from langgraph.graph import START,END, StateGraph

#graph_builder = StateGraph(State).add_sequence(
#    [write_query, execute_query, generate_answer]
#)
#graph_builder.add_edge(START, "write_query")
#graph = graph_builder.compile()

graph_builder = StateGraph(State)
graph_builder.add_node("write_query", write_query)
graph_builder.add_node("execute_query", execute_query)
graph_builder.add_node("generate_answer", generate_answer)

graph_builder.add_edge(START, "write_query")
graph_builder.add_edge("write_query", "execute_query")
graph_builder.add_edge("execute_query", "generate_answer")
graph_builder.add_edge("generate_answer", END)
graph = graph_builder.compile()

#%%
# from IPython.display import Image, display

# display(Image(graph.get_graph().draw_mermaid_png()))



def get_answer(question: str, explanation_text: str):
    return graph.invoke({"question": question, "explanation_text": explanation_text}).get("answer")

#get_answer("what is user_id 2's name?")





# Now , we need to use the text to good use and get the answer from the database.

# %%

def qa_functionality(tables_data):
    """Function to handle Q&A functionality in Streamlit."""
    st.header("Ask a Question")
    
    # Display the structure of the tables and their columns
    explanation_text = get_db_description(tables_data)
    #st.markdown(explanation_text)
    
    # Input for the user's question with a unique key
    question = st.text_input("Type your question here:", key="user_question_input")
    
    # Button to get the answer
    if st.button("Get Answer"):
        if question:
            answer = get_answer(question, explanation_text)  # Call the function to get the answer
            st.markdown(answer)  # Display the answer in markdown format
        else:
            st.warning("Please enter a question.")  # Warning if no question is entered
