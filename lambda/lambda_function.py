"""AWS Lambda: fetch one day of weather for a few Indian cities from Open-Meteo
and write it as a CSV file to S3 (raw/weather/). Athena reads that folder.

Environment variable: BUCKET = name of the S3 bucket.
Uses only the standard library and boto3 (already included in the Lambda runtime).
"""
import csv
import io
import json
import os
import urllib.request
from datetime import date, timedelta

import boto3

s3 = boto3.client("s3")

CITIES = {
    "Delhi": (28.61, 77.21),
    "Gurugram": (28.46, 77.03),
    "Mumbai": (19.08, 72.88),
}
LAG_DAYS = 7  # the archive API publishes data a few days late
URL = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude={lat}&longitude={lon}&start_date={day}&end_date={day}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    "&timezone=Asia%2FKolkata"
)


def fetch_city(city, lat, lon, day):
    url = URL.format(lat=lat, lon=lon, day=day)
    with urllib.request.urlopen(url, timeout=30) as response:
        daily = json.load(response)["daily"]
    return [
        city,
        daily["time"][0],
        daily["temperature_2m_max"][0],
        daily["temperature_2m_min"][0],
        daily["precipitation_sum"][0],
    ]


def lambda_handler(event, context):
    bucket = os.environ["BUCKET"]
    day = (date.today() - timedelta(days=LAG_DAYS)).isoformat()

    rows = [fetch_city(city, lat, lon, day) for city, (lat, lon) in CITIES.items()]

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["city", "obs_date", "temp_max_c", "temp_min_c", "rain_mm"])
    writer.writerows(rows)

    # One file per day: running twice for the same day overwrites, so no duplicates.
    key = "raw/weather/weather_{}.csv".format(day)
    s3.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue().encode("utf-8"))

    print("Wrote", len(rows), "rows to s3://{}/{}".format(bucket, key))
    return {"status": "ok", "key": key, "rows": len(rows)}
