#%%
from google.cloud import firestore
import os


#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "erudo_service_account_key.json"
#db = firestore.Client(database='erudo-operations', project='erudohq-dev')


def upload_dataset_schema(dataset: dict, database: str, project: str):
    """
    Uploads a full dataset schema to Firestore.

    dataset: {
        "name": str,
        "description": str,
        "tables": {
            "table_name": {
                "columns": {
                    "column_name": {
                        "description": str,
                        "type": str
                    },
                    ...
                }
            },
            ...
        }
    }
    """
    db = firestore.Client(database=database, project=project)
    dataset_id = dataset.get("name")
    if not dataset_id or "tables" not in dataset:
        raise ValueError("Dataset must include 'name' and 'tables'.")

    # Save the dataset-level document
    dataset_doc = {
        "name": dataset_id,
        "description": dataset.get("description", ""),
        "created_at": firestore.SERVER_TIMESTAMP
    }

    db.collection("datasets").document(dataset_id).set(dataset_doc)

    # Save each table as a document in the tables subcollection
    for table_name, table_info in dataset["tables"].items():
        db.collection("datasets").document(dataset_id).collection("tables").document(table_name).set(table_info)

    print(f"Schema for '{dataset_id}' uploaded successfully to Firestore.")

def fetch_dataset_details(dataset_id: str,database: str, project: str):
    """
    Fetches the complete details of a dataset from Firestore.

    dataset_id: str
    
    """
    db = firestore.Client(database=database, project=project)
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