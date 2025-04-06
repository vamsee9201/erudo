#%%
from google.cloud import firestore
import os

# Set Firestore credentials (update your path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "erudo_service_account_key.json"
db = firestore.Client(database='erudo-operations', project='erudohq-dev')


def upload_dataset_schema(dataset: dict):
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

user_orders_dataset = {
        "name": "user_orders",
        "description": "Dataset with user and order information",
        "tables": {
            "orders": {
                "columns": {
                    "order_id": {"description": "Unique identifier for the order", "type": "string"},
                    "user_id": {"description": "ID of the user who placed the order", "type": "string"},
                    "product": {"description": "Product name", "type": "string"},
                    "amount": {"description": "Order amount in USD", "type": "float"},
                    "order_date": {"description": "Date of the order", "type": "date"},
                }
            },
            "users": {
                "columns": {
                    "user_id": {"description": "Unique identifier for the user", "type": "string"},
                    "name": {"description": "Full name of the user", "type": "string"},
                    "email": {"description": "Email address of the user", "type": "string"},
                }
            }
        }
    }

upload_dataset_schema(user_orders_dataset)


# %%
