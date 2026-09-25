from fastapi import FastAPI
from main import load_leads, save_leads
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException

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