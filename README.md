# Norwegian Weather Data Collector
## What it gets

- Temperature and solar radiation (Frost API)
- Snow depth (Open-Meteo)
- Cloud cover
## Setup

```bash
pip install requests pandas
python weather_collector.py
```
You'll need a Frost API client ID from https://frost.met.no/

## Output

CSVs saved to `weather_data/` with timestamp, radiation, temp, snow depth, and cloud cover columns.

## Notes

The script goes back 5 days from today because Open-Meteo's archive has a delay. Snow data defaults to zero if unavailable.


© 2025 - Not licensed for reuse
