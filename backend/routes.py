import os
from fastapi import APIRouter
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

ROOT_ENV = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ROOT_ENV)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
router = APIRouter()

from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    question: str

class GenerateRequest(BaseModel):
    party1_name: Optional[str] = ""
    party1_address: Optional[str] = ""
    party2_name: Optional[str] = ""
    party2_address: Optional[str] = ""
    terms: Optional[str] = ""
    purpose: Optional[str] = ""
    doc_type: Optional[str] = "rental agreement"

@router.post("/ask")
async def ask_legal(q: Question):
    try:
        res = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": q.question}]
        )
        return {"answer": res.choices[0].message.content}
    except Exception as e:
        return {"answer": f"Error: {e}"}

@router.post("/generate")
async def generate_doc(req: GenerateRequest):
    try:
        prompt = f"Create a {req.doc_type} with Party1 {req.party1_name}, {req.party1_address} and Party2 {req.party2_name}, {req.party2_address}. Purpose: {req.purpose}. Terms: {req.terms}"
        res = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"document": res.choices[0].message.content}
    except Exception as e:
        return {"document": f"Error: {e}"}
