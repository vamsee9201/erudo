from fastapi import FastAPI

app = FastAPI()

@app.get("/answer")
def get_answer():
    return {"answer": "This is the answer!"}
