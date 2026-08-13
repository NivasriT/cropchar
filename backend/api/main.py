from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path
from backend.data_pipeline.match import run_pipeline_demo
from backend.core.config import settings
from backend.data_pipeline.match import run_pipeline
from backend.data_pipeline.offenders import update_offender_log
from backend.alerts.notifier import send_alert_email
from backend.alerts.alert_log import make_detection_id, already_sent, mark_sent

BASE_DIR = Path(__file__).resolve().parents[2]
OFFENDER_LOG = BASE_DIR / "data" / "offender_log.json"

app = FastAPI(
    title="CropChar API",
    description="Crop Residue & Unauthorized Burning Monitoring Backend API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_check():
    settings.validate()

@app.get("/")
def health_check():
    return {"status": "ok", "service": "CropChar API"}

@app.get("/hotspots")
def get_hotspots():
    try:
        result = run_pipeline()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Missing data file: {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Pipeline failed: {e}")

    update_offender_log(result)

    records = []
    for _, row in result.iterrows():
        records.append({
            "field_id": row.get("field_id"),
            "latitude": row.geometry.y,
            "longitude": row.geometry.x,
            "acq_date": row.get("acq_date"),
            "acq_time": row.get("acq_time"),
            "confidence": row.get("confidence"),
            "unauthorized": bool(row.get("unauthorized")),
        })
    return records

@app.get("/offenders")
def get_offenders():
    if not OFFENDER_LOG.exists():
        return []
    try:
        data = json.loads(OFFENDER_LOG.read_text())
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="offender_log.json is corrupted")

    return [{"field_id": fid, "unauthorized_count": count}
             for fid, count in data.items() if count > 1]

class AlertRequest(BaseModel):
    field_id: str
    acq_date: str
    to_email: str
    latitude: float = None
    longitude: float = None

@app.post("/alerts/trigger")
def trigger_alert(request: AlertRequest):
    detection_id = None
    if request.latitude is not None and request.longitude is not None:
        detection_id = make_detection_id(
            request.field_id, request.acq_date, request.latitude, request.longitude
        )
        if already_sent(detection_id):
            return {"status": "skipped", "reason": "Alert already sent for this detection"}

    try:
        send_alert_email(request.to_email, request.field_id, request.acq_date)
        if detection_id:
            mark_sent(detection_id)
        return {"status": "sent", "field_id": request.field_id, "acq_date": request.acq_date}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
@app.get("/hotspots/demo")
def get_hotspots_demo():
    """Returns matched+flagged results from sample data. Used when live FIRMS has no detections."""
    try:
        result = run_pipeline_demo()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Demo pipeline failed: {e}")

    update_offender_log(result)

    records = []
    for _, row in result.iterrows():
        records.append({
            "field_id": row.get("field_id"),
            "latitude": row.geometry.y,
            "longitude": row.geometry.x,
            "acq_date": row.get("acq_date"),
            "acq_time": row.get("acq_time") if "acq_time" in row else None,
            "confidence": row.get("confidence") if "confidence" in row else None,
            "unauthorized": bool(row.get("unauthorized")),
        })
    return records