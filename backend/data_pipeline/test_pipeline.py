import geopandas as gpd
import pandas as pd
from match import hotspots_to_geodf, match_to_fields, flag_unauthorized

hotspots = pd.read_csv("data/sample_hotspots.csv")
fields = gpd.read_file("data/sample_boundaries.geojson")
permits = pd.read_csv("data/permits_mock.csv")

hotspots_gdf = hotspots_to_geodf(hotspots)
matched = match_to_fields(hotspots_gdf, fields)
flagged = flag_unauthorized(matched, permits)

print(flagged[["field_id", "acq_date", "unauthorized"]])