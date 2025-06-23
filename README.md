# Greater Sydney SA2 Analysis

This project analyzes Statistical Area Level 2 (SA2) regions in Greater Sydney using multiple datasets and the NSW Points of Interest API.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ with PostGIS extension
- Access to NSW Points of Interest API

## Setup

1. Install PostgreSQL and PostGIS:

   ```bash
   # For macOS using Homebrew
   brew install postgresql
   brew install postgis
   ```

2. Create a PostgreSQL database:

   ```bash
   createdb sydney_analysis
   psql sydney_analysis
   CREATE EXTENSION postgis;
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Update database credentials in `db_setup.py`:
   ```python
   DB_PARAMS = {
       'host': 'localhost',
       'database': 'sydney_analysis',
       'user': 'your_username',
       'password': 'your_password'
   }
   ```

## Data Import

1. Download the SA2 digital boundaries from the ABS website
2. Place all data files in the project directory:

   - SA2 shapefile
   - Businesses.csv
   - Stops.txt
   - Schools shapefile
   - Population.csv
   - Income.csv

3. Run the database setup script:
   ```bash
   python db_setup.py
   ```

## Collecting Points of Interest

To collect Points of Interest for a specific SA4 region:

```bash
python poi_collector.py
```

Edit the SA4 code in the script to match your target region.

## Project Structure

- `db_setup.py`: Database setup and data import functions
- `poi_collector.py`: Points of Interest API integration
- `requirements.txt`: Python dependencies
- Data files:
  - SA2 boundaries
  - Businesses data
  - Public transport stops
  - Schools data
  - Population data
  - Income data

## Notes

- The NSW Points of Interest API has rate limits, so the script includes a 1-second delay between requests
- All spatial data is stored in EPSG:4283 (GDA94) coordinate system
- Make sure to handle API keys and credentials securely
