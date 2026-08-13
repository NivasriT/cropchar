import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
MAP_KEY = os.getenv("FIRMS_MAP_KEY")
AREA = "77.745493,11.339389,77.752928,11.343442"
SOURCE = "VIIRS_SNPP_NRT"
DAYS = 3

url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/{SOURCE}/{AREA}/{DAYS}"

def fetch_hotspots():
    resp = requests.get(url)
    resp.raise_for_status()
    with open("data/raw_hotspots.csv", "w") as f:
        f.write(resp.text)
    df = pd.read_csv("data/raw_hotspots.csv")
    df = df[["latitude", "longitude", "acq_date", "acq_time", "confidence"]]
    df = df[df["confidence"].isin(["nominal", "high"])]
    return df

if __name__ == "__main__":
    df = fetch_hotspots()
    print(df.head())