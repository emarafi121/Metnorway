# Norway Historical Weather Data Analysis (2025)

Python pipeline to collect and merge hourly historical weather data from Norwegian meteorological stations. Designed for renewable energy analysis, particularly PV performance in snowy regions.

## Features

- **Temperature & Solar Radiation**: MET Norway Frost API
- **Snow Depth**: Open-Meteo Historical Archive
- **Cloud Cover**: MET Norway Frost API
- Merged into clean CSVs using pandas
- Handles API delays, timezones, and missing data
- Collects full year of hourly data (365 days)

## Stations

Data collected from 5 stations in western Norway:
- Tingvoll (62.90°N, 8.16°E)
- Brusdalen (62.46°N, 6.88°E)
- Surnadal Sylte (63.07°N, 8.93°E)
- Linge (62.47°N, 7.23°E)
- Vigra (62.56°N, 6.10°E)

## Requirements

```bash
pip install requests pandas
```

Python 3.7 or higher required.

## Usage

1. Get your Frost API Client ID from https://frost.met.no/
2. Add it to the script
3. Run: `python weather_collector.py`
4. Find output CSVs in `weather_data/` folder

## Output Format

Each CSV contains:
- `timestamp` - Date and time (UTC)
- `global_radiation` - Solar radiation (W/m²)
- `air_temperature_c` - Air temperature (°C)
- `snow_depth_cm` - Snow depth (cm)
- `cloud_cover_percent` - Cloud coverage (%)

## Data Sources

- **Frost API** (MET Norway): Temperature, solar radiation, cloud cover
- **Open-Meteo Archive API**: Snow depth data

## Notes

- Data shifted 5 days back from current date due to Open-Meteo Archive delay
- 1-second delay between API requests for rate limiting
- Missing snow data filled with zeros

## License

All rights reserved. This code is for viewing purposes only and may not be copied, modified, or distributed without permission.
