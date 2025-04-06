from fastapi import FastAPI, HTTPException
from bq_utils import get_tables_and_columns

app = FastAPI()

# Define the project ID as a variable
PROJECT_ID = "erudohq-dev"  # Replace with your actual project ID

@app.get("/ask")
async def ask_question(question: str):
    # Simple response logic (replace with your own logic if needed)
    answer = f"You asked: '{question}', and here's a simple response."
    return {"answer": answer}

@app.get("/bigquery/{dataset_id}")
async def get_bigquery_details(dataset_id: str):
    try:
        details = get_tables_and_columns(PROJECT_ID, dataset_id)
        return {"tables": details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






