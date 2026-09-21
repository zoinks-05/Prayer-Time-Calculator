from prayertimes import prayerTimes


TEST_CASES = [
    # Normal — Sydney
    {
        "name": "Sydney",
        "year": 2026,
        "month": 6,
        "day": 21,
        "timezone": 10,
        "long": 151.2094,
        "lat": -33.8688,
        "method": 2,
    },

    # Sydney summer / DST
    {
        "name": "Sydney Summer",
        "year": 2026,
        "month": 12,
        "day": 21,
        "timezone": 11,
        "long": 151.2094,
        "lat": -33.8688,
        "method": 2,
    },

    # Equator
    {
        "name": "Singapore",
        "year": 2026,
        "month": 3,
        "day": 21,
        "timezone": 8,
        "long": 103.8198,
        "lat": 1.3521,
        "method": 2,
    },

    # Makkah
    {
        "name": "Makkah",
        "year": 2026,
        "month": 3,
        "day": 21,
        "timezone": 3,
        "long": 39.8579,
        "lat": 21.3891,
        "method": 1,
    },

    # London
    {
        "name": "London",
        "year": 2026,
        "month": 6,
        "day": 21,
        "timezone": 1,
        "long": -0.1278,
        "lat": 51.5074,
        "method": 2,
    },

    # Tromsø — summer
    {
        "name": "Tromso Summer",
        "year": 2026,
        "month": 6,
        "day": 21,
        "timezone": 2,
        "long": 18.9553,
        "lat": 69.6492,
        "method": 2,
    },

    # Tromsø — equinox
    {
        "name": "Tromso Equinox",
        "year": 2026,
        "month": 9,
        "day": 21,
        "timezone": 2,
        "long": 18.9553,
        "lat": 69.6492,
        "method": 2,
    },

    # Tromsø — winter
    {
        "name": "Tromso Winter",
        "year": 2026,
        "month": 12,
        "day": 21,
        "timezone": 1,
        "long": 18.9553,
        "lat": 69.6492,
        "method": 2,
    },

    # Longyearbyen — summer
    {
        "name": "Longyearbyen Summer",
        "year": 2026,
        "month": 6,
        "day": 21,
        "timezone": 2,
        "long": 15.6469,
        "lat": 78.2232,
        "method": 2,
    },

    # Longyearbyen — winter
    {
        "name": "Longyearbyen Winter",
        "year": 2026,
        "month": 12,
        "day": 21,
        "timezone": 1,
        "long": 15.6469,
        "lat": 78.2232,
        "method": 2,
    },

    # Ushuaia — southern high latitude
    {
        "name": "Ushuaia",
        "year": 2026,
        "month": 6,
        "day": 21,
        "timezone": -3,
        "long": -68.3030,
        "lat": -54.8019,
        "method": 2,
    },

    # New York
    {
        "name": "New York",
        "year": 2026,
        "month": 6,
        "day": 21,
        "timezone": -4,
        "long": -74.0060,
        "lat": 40.7128,
        "method": 2,
    },

    # Cairo
    {
        "name": "Cairo",
        "year": 2026,
        "month": 3,
        "day": 21,
        "timezone": 2,
        "long": 31.2357,
        "lat": 30.0444,
        "method": 3,
    },

    # Karachi
    {
        "name": "Karachi",
        "year": 2026,
        "month": 3,
        "day": 21,
        "timezone": 5,
        "long": 67.0011,
        "lat": 24.8607,
        "method": 5,
    },
]


def run_tests():

    print("=" * 60)
    print("PRAYER TIMES TEST SUITE")
    print("=" * 60)

    for test in TEST_CASES:

        print(f"\n--- {test['name']} ---")

        times = prayerTimes(
            test["year"],
            test["month"],
            test["day"],
            test["timezone"],
            test["long"],
            test["lat"],
            method=test["method"],
        )

        print(
            f"Date: {test['year']}-{test['month']:02d}-{test['day']:02d}"
        )
        print(
            f"Location: {test['lat']}°, {test['long']}°"
        )
        print(f"Timezone: UTC{test['timezone']:+}")
        print(f"Method: {test['method']}")

        for prayer, time in times.items():
            print(f"{prayer:8}: {time}")


if __name__ == "__main__":
    run_tests()