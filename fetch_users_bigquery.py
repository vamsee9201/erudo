import os  # Import the os module

# Set the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "erudo_service_account_key.json"  # Update with your JSON key file path

from google.cloud import bigquery

def fetch_users_data(project_id, dataset_id):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # SQL query to fetch all data from the users table
    query = f"SELECT * FROM `{project_id}.{dataset_id}.users`"

    # Execute the query and fetch the results
    query_job = client.query(query)
    results = query_job.result()  # Wait for the job to complete

    # Print the results
    for row in results:
        print(dict(row))  # Convert each row to a dictionary for better readability

# Example usage
project_id = "erudohq-dev"  # Replace with your Google Cloud project ID
dataset_id = "user_orders"    # Replace with your BigQuery dataset ID

fetch_users_data(project_id, dataset_id) 