# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import os

# Firebase + Firestore setup
import firebase_admin
from firebase_admin import credentials, firestore

# Step 1: Load credentials from your service account JSON
SERVICE_ACCOUNT_PATH = "service-account.json"

if not os.path.exists(SERVICE_ACCOUNT_PATH):
    raise RuntimeError("Missing service-account.json in project root")

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)

# Step 2: Initialize Firebase app if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'projectId': os.getenv("GOOGLE_CLOUD_PROJECT")
    })

# Step 3: Firestore client
db = firestore.client()
prompts_collection = db.collection("prompts")

# Step 4: FastAPI instance
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "PromptOps API v0.1 alive"}

# Input model (request body)
class PromptCreate(BaseModel):
    title: str
    content: str

# Output model (response body)
class Prompt(BaseModel):
    id: str
    title: str
    content: str

# Step 5: Create prompt
@app.post("/prompts", response_model=Prompt)
def create_prompt(prompt: PromptCreate):
    new_id = str(uuid.uuid4())
    prompt_data = {
        "id": new_id,
        "title": prompt.title,
        "content": prompt.content,
    }
    prompts_collection.document(new_id).set(prompt_data)
    return Prompt(**prompt_data)

# Step 6: List all prompts
@app.get("/prompts", response_model=List[Prompt])
def list_prompts():
    docs = prompts_collection.stream()
    return [Prompt(**doc.to_dict()) for doc in docs]

# Step 7: Retrieve a single prompt
@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    doc = prompts_collection.document(prompt_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return Prompt(**doc.to_dict())
