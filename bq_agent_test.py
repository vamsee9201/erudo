#%%
from google.cloud import bigquery
from google.cloud import firestore  # Import Firestore
import os
from langchain.chat_models import init_chat_model
import json
#%%
#This method is used to execute a query on BigQuery and return the results as a list of dictionaries

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'erudo_service_account_key.json'
llm = init_chat_model("gpt-4o-mini", model_provider="openai")
#%%
with open('openai_key.json', 'r') as file:
    data = json.load(file)
os.environ['OPENAI_API_KEY'] = data["api_key"]

#%%
def execute_query(project_id, query):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Execute the query
    query_job = client.query(query)
    
    # Wait for the job to complete and return the results
    results = query_job.result()
    
    return [dict(row) for row in results] 
#%%
query = "SELECT * FROM `erudohq-dev.user_orders.orders` LIMIT 1000"
results = execute_query("erudohq-dev",query)
print(results)
#%%
#todo items
#create an get explanation text function. Where we would pass in the table and columns data, it should return the explanation text.(done)
#Using that create a write query function. 
#Make sure the write query function is able to write big query sql style query. 
#Create a graph and test it.
# integrate the graph in the fastapi server. 
sample_explanation_json = {
  "orders": {
    "description": "This table stores information about each order placed by users.",
    "columns": {
      "order_id": "Unique identifier for each order.",
      "user_id": "Identifier for the user who placed the order. References the users table.",
      "product": "Name or identifier of the product ordered.",
      "amount": "Total monetary value of the order.",
      "order_date": "Date when the order was placed."
    }
  },
  "users": {
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


def write_query(question,data):
    """Generate SQL query to fetch information."""
    # Updated prompt to include explanation text and database details
    explanation_text = get_explanation_text(data)
    prompt = (
        f"Write a big query SQL query to answer the question: '{question}'. "
        f"Use the following explanation text to help you write the query: {explanation_text}"
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)

    return {"query": result["query"]}
#%%
write_query("What is the total amount of orders for each user?",sample_explanation_json)
#%%
