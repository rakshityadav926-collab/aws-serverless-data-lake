"""Fetch daily weather for a few Indian cities from the Open-Meteo archive API
and save it as a CSV file. The same logic will later run inside AWS Lambda."""
import csv
import json
import urllib.request

CITIES = {
    "Delhi": (28.61, 77.21),
    "Gurugram": (28.46, 77.03),
    "Mumbai": (19.08, 72.88),
}
START_DATE = "2026-10-01"
END_DATE = "2026-10-31"
URL = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    "&timezone=Asia%2FKolkata"
)


def fetch_city(city, lat, lon):
    url = URL.format(lat=lat, lon=lon, start=START_DATE, end=END_DATE)
    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.load(response)
    daily = data["daily"]
    rows = []
    for i, day in enumerate(daily["time"]):
        rows.append({
            "city": city,
            "date": day,
            "temp_max_c": daily["temperature_2m_max"][i],
            "temp_min_c": daily["temperature_2m_min"][i],
            "rain_mm": daily["precipitation_sum"][i],
        })
    return rows


def main():
    all_rows = []
    for city, (lat, lon) in CITIES.items():
        all_rows.extend(fetch_city(city, lat, lon))

    with open("weather.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["city", "date", "temp_max_c", "temp_min_c", "rain_mm"]
        )
        writer.writeheader()
        writer.writerows(all_rows)
    print("Saved", len(all_rows), "rows to weather.csv")


if __name__ == "__main__":
    main()
