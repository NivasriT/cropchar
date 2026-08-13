import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_PATH = BASE_DIR / "data" / "offender_log.json"


def update_offender_log(flagged_gdf):
    log = {}

    if LOG_PATH.exists():
        with open(LOG_PATH) as f:
            log = json.load(f)

    for _, row in flagged_gdf[flagged_gdf.unauthorized].iterrows():
        field_id = row["field_id"]
        log[field_id] = log.get(field_id, 0) + 1

    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

    return log