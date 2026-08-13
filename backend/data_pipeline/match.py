import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from rules import is_unauthorized
from fetch_firms import fetch_hotspots

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
    fields = gpd.read_file("data/sample_boundaries.geojson")
    permits = pd.read_csv("data/permits_mock.csv")
    hotspots_gdf = hotspots_to_geodf(hotspots)
    matched = match_to_fields(hotspots_gdf, fields)
    return flag_unauthorized(matched, permits)