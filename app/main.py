# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uuid

# Step 1: Create the FastAPI app instance
app = FastAPI()

# Step 2: Root endpoint
@app.get("/")
def read_root():
    return {"status": "PromptOps API v0.1 alive"}

# Step 3: Data model
class Prompt(BaseModel):
    id: str
    title: str
    content: str

# Step 4: In-memory storage
prompts: List[Prompt] = []

# Step 5: CRUD endpoints
@app.post("/prompts", response_model=Prompt)
def create_prompt(prompt: Prompt):
    prompt.id = str(uuid.uuid4())
    prompts.append(prompt)
    return prompt

@app.get("/prompts", response_model=List[Prompt])
def list_prompts():
    return prompts

@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    for p in prompts:
        if p.id == prompt_id:
            return p
    return {"error": "Prompt not found"}