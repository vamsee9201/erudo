from fastapi import FastAPI, HTTPException
from bq_utils import get_tables_and_columns
from fs_utils import upload_dataset_schema, fetch_dataset_details
from bq_agent import get_answer
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

@app.post("/upload-schema")
async def upload_schema(dataset: dict):
    try:
        database = 'erudo-operations'
        print("upload request received")
        upload_dataset_schema(dataset, 'erudo-operations',PROJECT_ID)
        return {"message": "Dataset schema uploaded successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dataset/{dataset_id}")
async def get_dataset_details(dataset_id: str):
    try:
        print(dataset_id)
        details = fetch_dataset_details(dataset_id, 'erudo-operations', PROJECT_ID)
        if details is None:
            raise HTTPException(status_code=404, detail="Dataset not found.")
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/get-answer")
async def get_answer(question: str, explanation_json: dict):
    answer = get_answer(question, explanation_json)
    return {"answer": answer}








