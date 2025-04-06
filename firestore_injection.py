#%%
from google.cloud import firestore
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "erudo_service_account_key.json"  # Update with your JSON key file path
db = firestore.Client(database='erudo-operations',project='erudohq-dev')
from bigquery_fetch import get_tables_and_columns  # Import the function to fetch tables and columns

# Updated dataset name
dataset_id = "user_orders"
dataset_doc = {
    "name": "user_orders",
    "description": "Dataset with user and order information",
    "created_at": firestore.SERVER_TIMESTAMP
}

# Initialize descriptions for columns
descriptions = {
    "orders": {
        "order_id": "Unique identifier for the order",
        "user_id": "ID of the user who placed the order",
        "product": "Product name",
        "amount": "Order amount in USD",
        "order_date": "Date of the order",
    },
    "users": {
        "user_id": "Unique identifier for the user",
        "name": "Full name of the user",
        "email": "Email address of the user",
    }
}

# Fetch tables and columns from BigQuery
project_id = "erudohq-dev"  # Replace with your Google Cloud project ID
dataset_id = "user_orders"    # Replace with your BigQuery dataset ID
table_schemas = get_tables_and_columns(project_id, dataset_id)  # Get schemas dynamically

# Create 'user_orders' dataset document
db.collection("datasets").document(dataset_id).set(dataset_doc)

# Add tables as documents inside 'tables' subcollection
for table_name, columns in table_schemas.items():
    schema = {"columns": {col: {"description": descriptions.get(table_name, {}).get(col, "No description available"), "type": "string"} for col in columns}}  # Use descriptions
    db.collection("datasets").document(dataset_id).collection("tables").document(table_name).set(schema)

print("Schema saved to Firestore under 'datasets/user_orders'.")

# %%
