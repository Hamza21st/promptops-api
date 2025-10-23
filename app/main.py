from fastapi import FastAPI

app = FastAPI(title="PromptOps API", version="0.1")

@app.get("/")
def read_root():
    return {"status": "PromptOps API v0.1 alive"}
