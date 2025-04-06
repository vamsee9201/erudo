#%%
from google.cloud import firestore
import os


#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "erudo_service_account_key.json"
#db = firestore.Client(database='erudo-operations', project='erudohq-dev')


def upload_dataset_schema(dataset: dict,database:str,project:str):
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
#%%



# %%
