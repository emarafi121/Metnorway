import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

CLIENT_ID = 'Put the actual Api Client ID here'

# Open Meteo archive lags about 5 days behind, so 5 days are adjusted for that reason
END_DATE = datetime.now() - timedelta(days=5) 
START_DATE = END_DATE - timedelta(days=365*5)

STATIONS = {
    'Tingvoll': {'id': 'SN64510', 'lat': 62.90, 'lon': 8.16},
    'Brusdalen': {'id': 'SN60875', 'lat': 62.46, 'lon': 6.88},
    'Surnadal Sylte': {'id': 'SN64760', 'lat': 63.07, 'lon': 8.93},
    'Linge': {'id': 'SN60650', 'lat': 62.47, 'lon': 7.23},
    'Vigra': {'id': 'SN60990', 'lat': 62.56, 'lon': 6.10},
}

HOURLY_ELEMENTS = [
    'mean(surface_downwelling_shortwave_flux_in_air PT1H)',
    'air_temperature',
    'cloud_area_fraction',
]


def fetch_frost_data(station_id, elements, start, end):
    url = 'https://frost.met.no/observations/v0.jsonld'
    
    params = {
        'sources': station_id,
        'elements': ','.join(elements),
        'referencetime': f'{start.strftime("%Y-%m-%dT%H:%M:%S")}/{end.strftime("%Y-%m-%dT%H:%M:%S")}',
        'timeresolutions': 'PT1H',
        'levels': 'default'
    }
    
    print(f"  Fetching temp/solar from Frost for {station_id}...")
    
    try:
        r = requests.get(url, params, auth=(CLIENT_ID, ''))
        r.raise_for_status()
        
        data = r.json()
        if 'data' not in data:
            return pd.DataFrame()
        
        records = []
        for obs in data['data']:
            record = {'timestamp': obs['referenceTime']}
            for o in obs['observations']:
                record[o['elementId']] = o['value']
            records.append(record)
        
        df = pd.DataFrame(records)
        
    
        df.rename(columns={
            'mean(surface_downwelling_shortwave_flux_in_air PT1H)': 'global_radiation', 
            'air_temperature': 'air_temperature_c',
            'cloud_area_fraction': 'cloud_cover_percent'
        }, inplace=True, errors='ignore')
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"  Frost API error: {e}")
        return pd.DataFrame()


def fetch_snow_depth(lat, lon, start, end):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start.strftime('%Y-%m-%d'),
        "end_date": end.strftime('%Y-%m-%d'),
        "hourly": "snow_depth", 
        "timezone": "UTC"
    }

    print(f"  Fetching snow depth from Open-Meteo...")
    
    try:
        r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)
        r.raise_for_status()
        
        data = r.json()
        hourly = data['hourly']
        
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(hourly['time'], utc=True),
            'snow_depth_cm': [d * 100 if d else 0 for d in hourly['snow_depth']]
        })
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"  Open-Meteo error: {e}")
        return pd.DataFrame()


def collect_station_data(name, info, start, end):
    print(f"\n{name}:")
    
    frost_df = fetch_frost_data(info['id'], HOURLY_ELEMENTS, start, end)
    if frost_df.empty:
        print(f"  Failed to get Frost data, skipping")
        return None
    
    snow_df = fetch_snow_depth(info['lat'], info['lon'], start, end)
    
    if snow_df.empty:
        print(f"  No snow data, filling with zeros")
        frost_df['snow_depth_cm'] = 0.0
        combined = frost_df
    else:
        combined = pd.merge(frost_df, snow_df, on='timestamp', how='left')
    
    
    cols = ['timestamp', 'global_radiation', 'air_temperature_c', 'snow_depth_cm', 'cloud_cover_percent']
    combined = combined[[c for c in cols if c in combined.columns]]
    
    return combined


def main():
    output_dir = 'weather_data'
    os.makedirs(output_dir, exist_ok=True)
    
    for name, info in STATIONS.items():
        df = collect_station_data(name, info, START_DATE, END_DATE)
        
        if df is not None:
            filename = f"{output_dir}/{name.lower().replace(' ', '_')}.csv"
            df.to_csv(filename, index=False)
            print(f"  Saved {len(df)} records to {filename}")
        
        time.sleep(1)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
