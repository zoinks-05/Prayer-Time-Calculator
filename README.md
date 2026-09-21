# Prayer Time Calculator

A Python prayer time calculator and REST API built with FastAPI.

It calculates Islamic prayer times using astronomical calculations based on:

* Date
* Latitude
* Longitude
* Timezone
* Calculation method

The API does not determine or guess the user's location or timezone. These are provided by the client.

## Prayer Times

The calculator provides:

* Fajr
* Sunrise
* Dhuhr
* Asr
* Maghrib
* Isha

## Calculation Methods

| ID | Method                               |
| -- | ------------------------------------ |
| 1  | Umm al-Qura                          |
| 2  | Muslim World League                  |
| 3  | Egyptian General Authority of Survey |
| 4  | ISNA                                 |
| 5  | Karachi                              |

High-latitude locations are automatically handled when normal astronomical calculations cannot produce a prayer time.

## API

### Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

### Get Prayer Times

```text
GET /prayertimes/{year}/{month}/{day}/{timezone}/{long}/{lat}/{method}
```

Example:

```text
/prayertimes/2026/9/21/10/151.2094/-33.8688/2
```

Returns:

```json
{
    "date": "2026-09-21",
    "location": {
        "latitude": -33.8688,
        "longitude": 151.2094,
        "timezone": 10
    },
    "method": 2,
    "status": "ok",
    "fallback_required": false,
    "prayer_times": {
        "Fajr": "05:12",
        "Sunrise": "06:30",
        "Dhuhr": "12:00",
        "Asr": "15:20",
        "Maghrib": "17:30",
        "Isha": "18:50"
    }
}
```

### Multiple Days

```text
GET /prayertimes/getalot/{year}/{month}/{day}/{timezone}/{long}/{lat}/{method}/{no_of_days}
```

Example:

```text
/prayertimes/getalot/2026/9/21/10/151.2094/-33.8688/2/30
```

Calculates prayer times for 30 days starting from the given date.

## Project Structure

```text
Prayer-Time-Calculator/
├── scripts/
│   └── prayertimes.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## References

* [PrayTimes Python implementation](https://gist.github.com/zsmahi/3761923)
* [A Geophysical Analysis Through a Python Program to Predict Sunrise, Sunset and Prayer Timings](https://www.researchgate.net/publication/377527508_A_Geophysical_Analysis_Through_a_Python_Program_to_Predict_Sunrise_Sunset_and_Prayer_Timings)

The project uses these references to guide the astronomical calculations and prayer-time methodology.
