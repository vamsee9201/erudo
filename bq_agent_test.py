#%%
from google.cloud import bigquery
from google.cloud import firestore  # Import Firestore
import os
from langchain.chat_models import init_chat_model
import json
#%%
#This method is used to execute a query on BigQuery and return the results as a list of dictionaries
with open('openai_key.json', 'r') as file:
    data = json.load(file)
os.environ['OPENAI_API_KEY'] = data["api_key"]

PROJECT_ID = "erudohq-dev"
#%%
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'erudo_service_account_key.json'
llm = init_chat_model("gpt-4o-mini", model_provider="openai")
#%%
def get_query_result(project_id, query):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Execute the query
    query_job = client.query(query)
    
    # Wait for the job to complete and return the results
    results = query_job.result()
    
    return [dict(row) for row in results] 
#%%
query = "SELECT * FROM `erudohq-dev.user_orders.orders` LIMIT 1000"
results = get_query_result("erudohq-dev",query)
print(results)
#%%
#todo items
#create an get explanation text function. Where we would pass in the table and columns data, it should return the explanation text.(done)
#Using that create a write query function. 
#Make sure the write query function is able to write big query sql style query. 
#Create a graph and test it.
# integrate the graph in the fastapi server. 
sample_explanation_json = {
  "erudohq-dev.user_orders.orders": {
    "description": "This table stores information about each order placed by users.",
    "columns": {
      "order_id": "Unique identifier for each order.",
      "user_id": "Identifier for the user who placed the order. References the users table.",
      "product": "Name or identifier of the product ordered.",
      "amount": "Total monetary value of the order.",
      "order_date": "Date when the order was placed."
    }
  },
  "erudohq-dev.user_orders.users": {
    "description": "This table contains user profile information.",
    "columns": {
      "user_id": "Unique identifier for each user.",
      "name": "Full name of the user.",
      "email": "Email address of the user."
    }
  }
}
#%%
def get_explanation_text(data):
    explanation = []
    for table, info in data.items():
        explanation.append(f"Table: {table}\n")
        explanation.append(f"{info['description']}\n")
        for column, description in info['columns'].items():
            explanation.append(f"{column}: {description}\n")
    return ''.join(explanation)

get_explanation_text(sample_explanation_json)
#%%

from typing_extensions import Annotated
from typing_extensions import TypedDict


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

#%%
from typing_extensions import TypedDict
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    explanation_json : dict
#%%
def write_query(state: State):
    """Generate SQL query to fetch information."""
    # Updated prompt to include explanation text and database details
    explanation_text = get_explanation_text(state["explanation_json"])
    prompt = (
        f"Write a big query SQL query to answer the question: '{state['question']}'. "
        f"Use the following explanation text to help you write the query: {explanation_text}"
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    #tempquery = "SELECT * FROM `erudohq-dev.user_orders.orders` LIMIT 1000"
    return {"query": result["query"]}
#%%
write_query({"question":"What is the total amount of orders for each user?", "explanation_json":sample_explanation_json})

#%%
def execute_query(state: State):
    """Execute SQL query."""
    query_result = get_query_result(project_id=PROJECT_ID, query=state["query"])
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



def get_answer(question: str, explanation_json: dict):
    result = graph.invoke({"question": question, "explanation_json": explanation_json})
    return result["answer"]

#%%
#graph.invoke({"question":"what did user_id 1 order?", "explanation_json":sample_explanation_json}))
#%%
get_answer("what did user_id 1 order?",sample_explanation_json)
#%%