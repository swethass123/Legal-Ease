from fastapi import APIRouter
router = APIRouter()

@router.post("/simplify")
async def simplify(data: dict):
    return {"result": "This is simplified legal text: " + data.get("text", "")[:200]}

@router.post("/summarize")
async def summarize(data: dict):
    return {"result": "Summary: " + data.get("text", "")[:200]}