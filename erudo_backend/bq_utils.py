from google.cloud import bigquery
from google.cloud import firestore  # Import Firestore
import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "erudo_service_account_key.json"  # Update with your JSON key file path

def get_tables_and_columns(project_id, dataset_id):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # Fetch the dataset
    dataset_ref = client.dataset(dataset_id)
    tables = client.list_tables(dataset_ref)

    result = {}

    # Loop through each table to get its schema
    for table in tables:
        table_name = table.table_id
        result[table_name] = []  # Initialize a list for columns
        
        # Fetch the table schema
        table_ref = dataset_ref.table(table_name)
        table_obj = client.get_table(table_ref)
        
        for schema_field in table_obj.schema:
            result[table_name].append(schema_field.name)  # Append column name to the list

    return result

def execute_query(project_id, query):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Execute the query
    query_job = client.query(query)
    
    # Wait for the job to complete and return the results
    results = query_job.result()
    
    return [dict(row) for row in results]  # Convert rows to dictionaries