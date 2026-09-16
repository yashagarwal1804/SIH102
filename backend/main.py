from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import ast
from sqlalchemy.orm import Session
from backend.database import engine
from backend.models import Investigation
from pydantic import BaseModel

app = FastAPI(
    title="MPLADS AI Anomaly Detection API",
    description="AI-powered risk monitoring system for MPLADS",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI results
df = pd.read_csv("data/explained_anomalies.csv")
@app.get("/")
def home():
    return {
        "message": "MPLADS AI Monitoring API is running",
        "status": "success"
    }
@app.get("/api/anomalies")
def get_anomalies():

    records = df.sort_values(
        "risk_score",
        ascending=False
    )

    results = []

    for _, row in records.iterrows():

        results.append({
            "constituency": row["constituency"],
            "year": int(row["year"]),
            "risk_score": round(float(row["risk_score"]), 2),
            "risk_category": row["risk_category"],
            "pending_works": int(row["pending_works"]),
            "pct_utilisation": float(row["pct_utilisation"]),
            "pct_completed": float(row["pct_completed"]),
            "reasons": ast.literal_eval(row["risk_reasons"])
        })

    return results


@app.get("/api/high-risk")
def get_high_risk():

    high_risk = df[
        df["risk_category"] == "HIGH"
    ].sort_values(
        "risk_score",
        ascending=False
    )

    results = []

    for _, row in high_risk.iterrows():

        results.append({
            "constituency": row["constituency"],
            "year": int(row["year"]),
            "risk_score": round(float(row["risk_score"]), 2),
            "risk_category": row["risk_category"],
            "pending_works": int(row["pending_works"]),
            "pct_utilisation": float(row["pct_utilisation"]),
            "pct_completed": float(row["pct_completed"]),
            "reasons": ast.literal_eval(row["risk_reasons"])
            })

    return results 
class InvestigationCreate(BaseModel):
          constituency: str
          year: int
          risk_score: float
          risk_category: str
          status: str
          officer_remarks: str | None = None
@app.get("/api/investigations")
def get_investigations():
    with Session(engine) as session:
        investigations = session.query(Investigation).all()

        return [
            {
                "id": item.id,
                "constituency": item.constituency,
                "year": item.year,
                "risk_score": item.risk_score,
                "risk_category": item.risk_category,
                "status": item.status,
                "officer_remarks": item.officer_remarks,
                "created_at": item.created_at
            }
            for item in investigations
        ]
        
        


@app.post("/api/investigations")
def create_investigation(data: InvestigationCreate):

    with Session(engine) as session:

        # Check whether this case already has an investigation
        investigation = (
            session.query(Investigation)
            .filter(
                Investigation.constituency == data.constituency,
                Investigation.year == data.year
            )
            .first()
        )

        # If it already exists, update it
        if investigation:

            investigation.status = data.status
            investigation.officer_remarks = data.officer_remarks

            session.commit()
            session.refresh(investigation)

            return {
                "message": "Investigation updated successfully",
                "id": investigation.id
            }

        # Otherwise create a new investigation
        investigation = Investigation(
            constituency=data.constituency,
            year=data.year,
            risk_score=data.risk_score,
            risk_category=data.risk_category,
            status=data.status,
            officer_remarks=data.officer_remarks
        )

        session.add(investigation)
        session.commit()
        session.refresh(investigation)

        return {
            "message": "Investigation created successfully",
            "id": investigation.id
        }


@app.put("/api/investigations/{investigation_id}")
def update_investigation(
    investigation_id: int,
    data: InvestigationCreate
):

    with Session(engine) as session:

        investigation = session.get(
            Investigation,
            investigation_id
        )

        if not investigation:
            return {
                "message": "Investigation not found"
            }

        investigation.status = data.status
        investigation.officer_remarks = data.officer_remarks

        session.commit()
        session.refresh(investigation)

        return {
            "message": "Investigation updated successfully",
            "id": investigation.id
        }