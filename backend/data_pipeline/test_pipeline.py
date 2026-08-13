import geopandas as gpd
import pandas as pd
from pathlib import Path
from backend.data_pipeline.match import hotspots_to_geodf, match_to_fields, flag_unauthorized

BASE_DIR = Path(__file__).resolve().parents[2]

hotspots = pd.read_csv(BASE_DIR / "data" / "sample_hotspots.csv")
fields = gpd.read_file(BASE_DIR / "data" / "sample_boundaries.geojson")
permits = pd.read_csv(BASE_DIR / "data" / "permits_mock.csv")

hotspots_gdf = hotspots_to_geodf(hotspots)
matched = match_to_fields(hotspots_gdf, fields)
flagged = flag_unauthorized(matched, permits)

print(flagged[["field_id", "acq_date", "unauthorized"]])