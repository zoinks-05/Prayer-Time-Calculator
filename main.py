from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scripts.prayertimes import prayerTimes
from datetime import date, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_inputs(year, month, day, timezone, long, lat, method):
    try:
        date(year, month, day)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date."
        )

    if not (-12 <= timezone <= 14):
        raise HTTPException(
            status_code=400,
            detail="Timezone must be between -12 and +14."
        )

    if not (-180 <= long <= 180):
        raise HTTPException(
            status_code=400,
            detail="Longitude must be between -180 and +180."
        )

    if not (-90 <= lat <= 90):
        raise HTTPException(
            status_code=400,
            detail="Latitude must be between -90 and +90."
        )

    if method not in [1, 2, 3, 4, 5]:
        raise HTTPException(
            status_code=400,
            detail="Method must be one of the following: 1, 2, 3, 4, or 5."
        )

def json_format(year, month, day, timezone, long, lat, method=2, times=None):
    fallback_required = any(
        value is None
        for value in times.values()
    )

    return {
        "date": date(year, month, day).isoformat(),
        "location": {
            "latitude": lat,
            "longitude": long,
            "timezone": timezone
        },
        "method": method,
        "status": "extreme_latitude" if fallback_required else "ok",
        "fallback_required": fallback_required,
        "prayer_times": times
    }

@app.get("/")
def root():
    return {"message": "Prayer Times API"}

@app.get("/prayertimes/")
def rt_prayertimes():
    return {"You are now using the Prayer Times API endpoint." : "Please provide the required parameters to get prayer times."}

@app.get("/prayertimes/test")
def test_prayertimes():
    year = 2026
    month = 9
    day = 21
    timezone = 10
    long = 151.2094
    lat = -33.8688

    times = prayerTimes(year, month, day, timezone, long, lat, method=2)

    return json_format(year, month, day, timezone, long, lat, method=2, times=times)

@app.get("/prayertimes/{year}/{month}/{day}/{timezone}/{long}/{lat}/{method}")
def get_prayertimes(year: int, month: int, day: int, timezone: float, long: float, lat: float, method: int = 2):
    validate_inputs(year, month, day, timezone, long, lat, method)  
    times = prayerTimes(year, month, day, timezone, long, lat, method)
    return json_format(year, month, day, timezone, long, lat, method, times)

@app.get("/prayertimes/getalot/{year}/{month}/{day}/{timezone}/{long}/{lat}/{method}/{no_of_days}")
def get_alot(year: int, month: int, day: int, timezone: float, long: float, lat: float, method: int = 2, no_of_days: int = 365):
    validate_inputs(year, month, day, timezone, long, lat, method)
    times = {}
    start = date(year, month, day).isoformat()
    for d in range(no_of_days):
        current_date = date(year, month, day) + timedelta(days=d)
        y = current_date.year
        m = current_date.month
        dy = current_date.day
        times[str(current_date)] = prayerTimes(y, m, dy, timezone, long, lat, method)
    return {"start_date": str(start), 
            "location": {
                "latitude": lat,
                "longitude": long,
                "timezone": timezone
            },
            "method": method,
            "number_of_days": no_of_days,
            "prayer_times": times,
            }
