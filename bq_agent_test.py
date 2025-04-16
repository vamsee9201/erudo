#%%
from google.cloud import bigquery
from google.cloud import firestore  # Import Firestore
import os
#%%
def execute_query(project_id, query):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Execute the query
    query_job = client.query(query)
    
    # Wait for the job to complete and return the results
    results = query_job.result()
    
    return [dict(row) for row in results] 


import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'erudo_service_account_key.json'
#%%
query = "SELECT * FROM `erudohq-dev.user_orders.orders` LIMIT 1000"
results = execute_query("erudohq-dev",query)
print(results)

# %%
from typing_extensions import TypedDict
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    explanation_text: str