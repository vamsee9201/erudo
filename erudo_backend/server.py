from fastapi import FastAPI

app = FastAPI()

@app.get("/ask")
async def ask_question(question: str):
    # Simple response logic (replace with your own logic if needed)
    answer = f"You asked: '{question}', and here's a simple response."
    return {"answer": answer}
