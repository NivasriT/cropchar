import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely.geometry import Point
from backend.data_pipeline.rules import is_unauthorized
from backend.data_pipeline.fetch_firms import fetch_hotspots

BASE_DIR = Path(__file__).resolve().parents[2]

def hotspots_to_geodf(hotspots_df):
    geometry = [Point(xy) for xy in zip(hotspots_df.longitude, hotspots_df.latitude)]
    return gpd.GeoDataFrame(hotspots_df, geometry=geometry, crs="EPSG:4326")

def match_to_fields(hotspots_gdf, fields_gdf):
    return gpd.sjoin(hotspots_gdf, fields_gdf, how="inner", predicate="within")

def flag_unauthorized(matched_gdf, permits_df):
    matched_gdf["unauthorized"] = matched_gdf.apply(
        lambda row: is_unauthorized(row["field_id"], row["acq_date"], permits_df),
        axis=1
    )
    return matched_gdf

def run_pipeline():
    hotspots = fetch_hotspots()
    fields = gpd.read_file(BASE_DIR / "data" / "sample_boundaries.geojson")
    permits = pd.read_csv(BASE_DIR / "data" / "permits_mock.csv")
    hotspots_gdf = hotspots_to_geodf(hotspots)
    matched = match_to_fields(hotspots_gdf, fields)
    return flag_unauthorized(matched, permits)
def run_pipeline_demo():
    hotspots = pd.read_csv(BASE_DIR / "data" / "sample_hotspots.csv")
    fields = gpd.read_file(BASE_DIR / "data" / "sample_boundaries.geojson")
    permits = pd.read_csv(BASE_DIR / "data" / "permits_mock.csv")
    hotspots_gdf = hotspots_to_geodf(hotspots)
    matched = match_to_fields(hotspots_gdf, fields)
    return flag_unauthorized(matched, permits)