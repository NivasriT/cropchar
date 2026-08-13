import geopandas as gpd

fields = gpd.read_file("data/sample_boundaries.geojson")

print(fields.head())
print(fields.crs)