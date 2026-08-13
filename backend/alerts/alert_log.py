import json
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parents[2] / "data" / "sent_alerts.json"

def _load():
    if not LOG_PATH.exists():
        return []
    return json.loads(LOG_PATH.read_text())

def _save(sent):
    LOG_PATH.write_text(json.dumps(sent, indent=2))

def make_detection_id(field_id, acq_date, latitude, longitude) -> str:
    return f"{field_id}_{acq_date}_{round(latitude, 4)}_{round(longitude, 4)}"

def already_sent(detection_id: str) -> bool:
    return detection_id in _load()

def mark_sent(detection_id: str) -> None:
    sent = _load()
    if detection_id not in sent:
        sent.append(detection_id)
        _save(sent)