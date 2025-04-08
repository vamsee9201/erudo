#%%
from google.cloud import firestore
import os
#%%
# Set Firestore credentials (update your path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "erudo_service_account_key.json"
db = firestore.Client(database='erudo-operations', project='erudohq-dev')

def fetch_dataset_details(dataset_id: str):
    """
    Fetches the complete details of a dataset from Firestore.

    dataset_id: str
    """
    try:
        dataset_ref = db.collection("datasets").document(dataset_id)
        dataset_doc = dataset_ref.get()

        if not dataset_doc.exists:
            print(f"No dataset found with ID: {dataset_id}")
            return None

        dataset_data = dataset_doc.to_dict()
        print(f"Dataset details for '{dataset_id}': {dataset_data}")

        # Fetching tables and their columns
        tables_ref = dataset_ref.collection("tables")
        tables_docs = tables_ref.stream()

        tables_data = {}
        for table in tables_docs:
            tables_data[table.id] = table.to_dict()

        # Combine dataset data with tables data
        complete_data = {
            "dataset": dataset_data,
            "tables": tables_data
        }

        return complete_data

    except Exception as e:
        print(f"Error fetching dataset details: {str(e)}")
        return None
#%%
# Example usage
if __name__ == "__main__":
    dataset_id = "user_orders"  # Replace with your dataset ID
    complete_details = fetch_dataset_details(dataset_id)
    print(complete_details)  # Print all details
# %% 