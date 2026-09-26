from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException
from ai_service import summarize_lead
from openai import APIError
from main import load_leads, save_leads, find_lead_by_id

app = FastAPI(title="Lead Manager API")

class LeadCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=254)
    message: str = Field(min_length=1, max_length=5000)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/leads")
def get_leads():
    return load_leads()

@app.post("/leads", status_code=201)
async def add_lead(data: LeadCreate):
    if "@" not in data.email or any(char.isspace() for char in data.email):
        raise HTTPException(
            status_code=422,
            detail="Email must contain @ and no whitespace.",
        )

    lead = {
        "id": str(uuid4()),
        "status": "new",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "name": data.name,
        "email": data.email,
        "message": data.message,
    }

    leads = load_leads()
    leads.append(lead)
    save_leads(leads)

    return lead

@app.post("/leads/summarize")
def summarize_request(data: LeadCreate):
    try:
        summary = summarize_lead(data.message)
    except APIError:
        raise HTTPException(
            status_code=502,
            detail="AI service unavailable. Please try again later.",
        )

    return {"summary": summary}

@app.post("/leads/{lead_id}/summary")
async def summarize_saved_lead(lead_id: str):
    leads = load_leads()
    lead = find_lead_by_id(leads, lead_id)

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found.")

    if lead.get("summary"):
        return lead

    try:
        summary = await run_in_threadpool(
            summarize_lead, lead["message"]
        )
    except APIError:
        raise HTTPException(
            status_code=502,
            detail="AI service unavailable. Please try again later.",
        )

    leads = load_leads()
    lead = find_lead_by_id(leads, lead_id)

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found.")

    lead["summary"] = summary
    save_leads(leads)

    return lead