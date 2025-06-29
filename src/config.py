import os

def debug(message: str):
    if os.getenv("DEBUG", "false").lower() == "true":
        print(f"DEBUG: {message}")

weekday_map = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

try:
    invite_day = weekday_map[os.getenv("INVITE_DAY", "Friday").lower()]
except KeyError:
    raise ValueError("Invalid INVITE_DAY. Must be one of: " + ", ".join(weekday_map.keys()))

api_key = os.getenv("WILLYWEATHER_API_KEY")
if not api_key:
    raise ValueError("WILLYWEATHER_API_KEY must be set")

location_id = os.getenv("WILLYWEATHER_LOCATION_ID")
if not location_id:
    raise ValueError("WILLYWEATHER_LOCATION_ID must be set")

attendees = os.getenv("ATTENDEES", "").split(",")
forecast_days = int(os.getenv("FORECAST_DAYS", 7))
earliest_tide = int(os.getenv("EARLIEST_TIDE", 7))
latest_tide = int(os.getenv("LATEST_TIDE", 17))
invite_hour, invite_minute = map(int, os.getenv("INVITE_TIME", "17:00").split(":"))
if invite_hour < 0 or invite_hour > 23 or invite_minute < 0 or invite_minute > 59:
    raise ValueError("Invalid invite time format. Use HH:MM in 24-hour format.")

debug(f"Configuration: invite_day={invite_day}, api_key={api_key}, "
      f"location_id={location_id}, attendees={attendees}, forecast_days={forecast_days}, "
      f"earliest_tide={earliest_tide}, latest_tide={latest_tide}, "
      f"invite_time={invite_hour}:{invite_minute}")