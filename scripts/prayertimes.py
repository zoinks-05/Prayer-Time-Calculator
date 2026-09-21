import math

#Note: 1-Umm al-Qura, 2-Muslim World League, 3-Egyptian General Authority of Survey, 4-ISNA, 5-Karachi

fajr_angles = {1: 18, 2: 18, 3: 19.5, 4: 15, 5: 18}
Isha_angles = {1: 17.5, 2: 17, 3: 17.5, 4: 15, 5: 18}

Adjustment_minutes = {
    1: {'Fajr': -2, 'Sunrise': 1, 'Dhuhr': 2, 'Asr': 3, 'Maghrib': 2, 'Isha': 0},
    2: {'Fajr': 1, 'Sunrise': 1, 'Dhuhr': 2, 'Asr': 2, 'Maghrib': 2, 'Isha': 2},
    3: {'Fajr': 0, 'Sunrise': 0, 'Dhuhr': 2, 'Asr': 2, 'Maghrib': 2, 'Isha': 3},
    4: {'Fajr': 1, 'Sunrise': 1, 'Dhuhr': 2, 'Asr': 2, 'Maghrib': 2, 'Isha': 2},
    5: {'Fajr': 1, 'Sunrise': 1, 'Dhuhr': 2, 'Asr': 2, 'Maghrib': 2, 'Isha': 2},
}

def julian_day(y,m,d):
    if m <= 2:
        y -= 1
        m += 12
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A/4)
    JD = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + B - 1524.5
    return JD

def julian_century(JD):
    return (JD - 2451545.0) / 36525.0

def Mean_Sun_Elements(T):
    L = 280.46646 + (36000.76983 * T) + (0.0003032 * T**2)
    L = L % 360

    M = 357.52911 + (35999.05029 * T) - (0.0001537 * T**2)
    M = M % 360

    e = 0.016708634 - (0.000042037 * T) - (0.0000001267 * T**2)

    return L, M, e

def equation_of_Center(T, M):
    Mrad = math.radians(M)
    C = (1.914602 - 0.004817 * T - 0.000014 * T**2) * math.sin(Mrad)
    C += (0.019993 - 0.000101 * T) * math.sin(2 * Mrad)
    C += 0.000289 * math.sin(3 * Mrad)
    return C

def apparent_Sun_Longitude(L, C, T):
    true_long = L + C
    rad = math.radians(125.04 - 1934.136 * T)
    apparent_long = true_long - 0.00568 - 0.00478 * math.sin(rad)
    return apparent_long

def obliquity(T):
    e0 = 23 + (26/60) + (21.448/3600)
    e0 -= (46.8150 * T + 0.00059 * T**2 - 0.001813 * T**3) / 3600
    rad = math.radians(125.04 - 1934.136 * T)
    e = e0 + 0.00256 * math.cos(rad)
    return e

def solar_declination(e, lambda_s):
    e_rad = math.radians(e)
    lambda_rad = math.radians(lambda_s)
    delta = math.asin(math.sin(e_rad) * math.sin(lambda_rad))
    return math.degrees(delta)

def EoT(e, L, M, epsilon):
    Mrad = math.radians(M)
    Lrad = math.radians(L)
    epsilon_rad = math.radians(epsilon)

    y = math.tan( epsilon_rad / 2)**2

    eot = (
        y * math.sin(2 * Lrad)
        - 2 * e * math.sin(Mrad)
        + 4 * e * y * math.sin(Mrad) * math.cos(2 * Lrad)
        - 0.5 * y**2 * math.sin(4 * Lrad)
        - 1.25 * e**2 * math.sin(2 * Mrad)
    )
    return math.degrees(eot) * 4 

def solarNoon(TZ, eot, longitude):
    SNcop = 15 * TZ - longitude
    SN = 12 + SNcop / 15 - eot / 60
    return SN

def solarAlt(lat, decline, hrAngle):
    rad_lat = math.radians(lat)
    rad_decline = math.radians(decline)
    rad_hrAngle = math.radians(hrAngle)
    sin_alt = (math.sin(rad_lat) * math.sin(rad_decline) +
               math.cos(rad_lat) * math.cos(rad_decline) * math.cos(rad_hrAngle))
    sin_alt = max(-1, min(1, sin_alt))
    return math.degrees(math.asin(sin_alt))

def hrAngle(lat, decline, alt):
    rad_lat = math.radians(lat)
    rad_decline = math.radians(decline)
    rad_alt = math.radians(alt)

    cosH = (
        math.sin(rad_alt)
        - math.sin(rad_lat) * math.sin(rad_decline)
    ) / (
        math.cos(rad_lat) * math.cos(rad_decline)
    )

    if cosH < -1 or cosH > 1:
        return None

    deltaT = math.degrees(math.acos(cosH)) / 15
    return deltaT

def shadowFactor(lat, decline, n=1):
    rad_lat = math.radians(lat)
    rad_decline = math.radians(decline)
    h_asr = math.atan(1/(n + math.tan(abs(rad_lat - rad_decline))))
    return math.degrees(h_asr)

def high_latitude_adjustment(sunriseTime, maghribTime, fajrAngle, ishaAngle):
    if sunriseTime is None or maghribTime is None:
        return {
            'Fajr': None,
            'Isha': None
        }

    nightLength = (24 - maghribTime) + sunriseTime

    fajrTime = sunriseTime - (nightLength * fajrAngle / 60)
    ishaTime = maghribTime + (nightLength * ishaAngle / 60)

    return {
        'Fajr': fajrTime % 24,
        'Isha': ishaTime % 24
    }

def timeConversion(time):
    if time is None:
        return None

    total_minutes = round(time * 60)
    total_minutes %= 24 * 60

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return f"{hours:02d}:{minutes:02d}"

def isRamadan(year, month, day):
    JD = julian_day(year, month, day)
    HM = int((JD - 1948439.5) / 29.53058867) % 12 + 1
    return HM == 9

def toHr(m):
    return m / 60.0

def solarData(year, month, day, long):
    JD = julian_day(year, month, day)
    T = julian_century(JD)

    L, M, e = Mean_Sun_Elements(T)
    C = equation_of_Center(T, M)
    lambda_s = apparent_Sun_Longitude(L, C, T)
    ecliptic_obliquity = obliquity(T)
    declination = solar_declination(ecliptic_obliquity, lambda_s)
    eot = EoT(e, L, M, ecliptic_obliquity)

    return declination, eot

def calculatePrayerTimes(solarNoon_time, declination, lat, method, year, month, day):
    sun_rad_refraction = 0.833

    fajrAngle = -fajr_angles[method]
    ishaAngle = -Isha_angles[method]

    fajr_deltaT = hrAngle(lat, declination, fajrAngle)
    isha_deltaT = hrAngle(lat, declination, ishaAngle)
    sunrise_deltaT = hrAngle(lat, declination, -sun_rad_refraction)

    asr_shadowFactor = shadowFactor(lat, declination, n=1)
    asr_deltaT = hrAngle(lat, declination, asr_shadowFactor)

    fajrTime = (
        None
        if fajr_deltaT is None
        else solarNoon_time - fajr_deltaT
    )

    sunriseTime = (
        None
        if sunrise_deltaT is None
        else solarNoon_time - sunrise_deltaT
    )

    dhuhrTime = solarNoon_time

    asrTime = (
        None
        if asr_deltaT is None
        else solarNoon_time + asr_deltaT
    )

    maghribTime = (
        None
        if sunrise_deltaT is None
        else solarNoon_time + sunrise_deltaT
    )

    if method == 1:
        if maghribTime is None:
            ishaTime = None
        elif isRamadan(year, month, day):
            ishaTime = maghribTime + 2
        else:
            ishaTime = maghribTime + 1.5
    else:
        ishaTime = (
            None
            if isha_deltaT is None
            else solarNoon_time + isha_deltaT
        )

    return {
        'Fajr': fajrTime,
        'Sunrise': sunriseTime,
        'Dhuhr': dhuhrTime,
        'Asr': asrTime,
        'Maghrib': maghribTime,
        'Isha': ishaTime
    }

def high_latitude_adjustment(sunriseTime, maghribTime, fajrAngle, ishaAngle):
    if sunriseTime is None or maghribTime is None:
        return {
            'Fajr': None,
            'Isha': None
        }

    nightLength = (24 - maghribTime) + sunriseTime

    fajrTime = sunriseTime - (nightLength * fajrAngle / 60)
    ishaTime = maghribTime + (nightLength * ishaAngle / 60)

    return {
        'Fajr': fajrTime % 24,
        'Isha': ishaTime % 24
    }

def applyHighLatitudeAdjustment(times, method):
    if times['Fajr'] is None or times['Isha'] is None:
        adjustedTimes = high_latitude_adjustment(
            times['Sunrise'],
            times['Maghrib'],
            fajr_angles[method],
            Isha_angles[method]
        )

        if times['Fajr'] is None:
            times['Fajr'] = adjustedTimes['Fajr']

        if times['Isha'] is None:
            times['Isha'] = adjustedTimes['Isha']

    return times

def formatPrayerTimes(times, method):
    formattedTimes = {}

    for prayer, time in times.items():
        if time is None:
            formattedTimes[prayer] = None
        else:
            formattedTimes[prayer] = timeConversion(
                time + toHr(Adjustment_minutes[method][prayer])
            )

    return formattedTimes

def prayerTimes(year, month, day, timezone, long, lat, method=2):
    declination, eot = solarData(year, month, day, long)

    solarNoon_time = solarNoon(
        timezone,
        eot,
        long
    )

    times = calculatePrayerTimes(
        solarNoon_time,
        declination,
        lat,
        method,
        year,
        month,
        day
    )

    times = applyHighLatitudeAdjustment(
        times,
        method
    )

    return formatPrayerTimes(
        times,
        method
    )

# test
if __name__ == "__main__":

    year = 2026
    month = 1
    day = 11
    timezone = 11
    long =  151.2094
    lat = -33.8688

    times = prayerTimes(year, month, day, timezone, long, lat, method=2)

    for prayer, time in times.items():
        print(f"{prayer}: {time}")