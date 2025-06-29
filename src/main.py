from datetime import datetime, timedelta
from gcal import *
from weather import *
import config
import time

__version__ = "0.1.0"

def invite_time(day: int, hour: int, min: int) -> bool:
    now = datetime.now()
    return now.weekday() == day and now.hour == hour and now.minute == min


def main():
    all_days = get_tide_forecast(config.api_key, config.location_id, config.forecast_days)

    if not all_days:
        print("No tide forecast data available.")
        return

    for day in all_days:
        date_str = day.get("dateTime")
        entries = day.get("entries", [])
        if not entries:
            continue

        low_tides = determine_low_tide(entries)
        if not low_tides:
            print(f"No low tides found for {date_str}")
            continue

        lowest_entry = min(low_tides, key=lambda e: e['height'])
        dt = datetime.strptime(lowest_entry['dateTime'], "%Y-%m-%d %H:%M:%S")

        minutes = (dt.minute + 7) // 15 * 15
        rounded_dt = dt.replace(minute=0, second=0) + timedelta(minutes=minutes)

        start_window_dt = max(rounded_dt - timedelta(hours=3),
                              rounded_dt.replace(hour=6, minute=0, second=0, microsecond=0))

        end_window_dt = min(rounded_dt + timedelta(hours=3),
                            rounded_dt.replace(hour=19, minute=0, second=0, microsecond=0))

        create_calendar_event(rounded_dt, start_window_dt, end_window_dt, lowest_entry['height'])

if __name__ == "__main__":
    if invite_time(config.invite_day, config.invite_hour, config.invite_minute):
        main()
    else:
        time.sleep(60)