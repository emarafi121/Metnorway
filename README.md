# Norwegian Weather Data Collector
Collects 5 years of hourly weather data from Norwegian stations for solar energy analysis.

## What it gets
- Temperature and solar radiation (Frost API)
- Snow depth (Open-Meteo)
- Cloud cover

## Setup
1. Get your Frost API client ID from https://frost.met.no/
2. Replace `'your-frost-api-client-id-here'` in the code with your actual ID
3. Install and run:

```bash
pip install requests pandas
python weather_collector.py
```

## Stations
Tingvoll, Brusdalen, Surnadal Sylte, Linge, Vigra

## Output
CSVs saved to `weather_data/` with timestamp, radiation, temp, snow depth, and cloud cover columns.

## Notes
Collects 5 years of historical data (goes back 5 days from today due to Open-Meteo delay). Snow data defaults to zero if unavailable.
© 2025 - Not licensed for reuse
