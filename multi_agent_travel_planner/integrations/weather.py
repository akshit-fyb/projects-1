import requests

def geocode(city):
    r=requests.get('https://geocoding-api.open-meteo.com/v1/search',params={'name':city,'count':1,'language':'en','format':'json'},timeout=8)
    r.raise_for_status(); results=r.json().get('results') or []
    return results[0] if results else None

def forecast(city):
    place=geocode(city)
    if not place: return {'available':False,'message':'Location not found'}
    r=requests.get('https://api.open-meteo.com/v1/forecast',params={'latitude':place['latitude'],'longitude':place['longitude'],'daily':'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max','forecast_days':7,'timezone':'auto'},timeout=8)
    r.raise_for_status(); d=r.json()['daily']
    days=[{'date':d['time'][i],'min_c':d['temperature_2m_min'][i],'max_c':d['temperature_2m_max'][i],'rain_probability':d['precipitation_probability_max'][i]} for i in range(len(d['time']))]
    return {'available':True,'source':'Open-Meteo (live forecast)','place':place.get('name',city),'days':days}
