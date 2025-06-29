from collections import defaultdict
from datetime import datetime
import json
import requests
import config

from datetime import datetime, timedelta
import json
import requests

def get_tide_forecast(api_key: str, location_id: str, forecast_days: int) -> list:
    url = f"https://api.willyweather.com.au/v2/{api_key}/locations/{location_id}/weather.json"
    all_days = []

    for i in range(forecast_days):
        start_date = (datetime.now().date() + timedelta(days=i)).isoformat()
        headers = {
            "Content-Type": "application/json",
            "x-payload": json.dumps({
                "forecasts": ["tides"],
                "days": 1,
                "startDate": start_date
            })
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        days = data.get("forecasts", {}).get("tides", {}).get("days", [])
        if days:
            all_days.append(days[0])

    return all_days


def determine_low_tide(entries: list):
    day_entries = defaultdict(list)

    for entry in entries:
        dt = datetime.strptime(entry['dateTime'], "%Y-%m-%d %H:%M:%S")
        if config.earliest_tide <= dt.hour < config.latest_tide:
            day_key = dt.date().isoformat()
            day_entries[day_key].append(entry)

    daily_lowest = []

    for day, day_list in day_entries.items():
        lowest_entry = min(day_list, key=lambda e: e['height'])
        daily_lowest.append(lowest_entry)

    return daily_lowest

