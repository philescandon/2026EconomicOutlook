"""
Data Manager for Economic Dashboard
Handles loading, saving, and refreshing economic data from FRED and BEA APIs.
"""

import os
import pandas as pd
import requests
from datetime import datetime
from pathlib import Path

# Try to import fredapi, handle if not installed
try:
    from fredapi import Fred
    FRED_AVAILABLE = True
except ImportError:
    FRED_AVAILABLE = False

# Data directory path
DATA_DIR = Path(__file__).parent / "data"


# =============================================================================
# CSV LOAD/SAVE FUNCTIONS
# =============================================================================

def load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV file from the data directory."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        return pd.read_csv(filepath)
    return None


def save_csv(df: pd.DataFrame, filename: str) -> None:
    """Save a DataFrame to CSV in the data directory."""
    DATA_DIR.mkdir(exist_ok=True)
    filepath = DATA_DIR / filename
    df.to_csv(filepath, index=False)


def get_last_updated(filename: str) -> str:
    """Get the last modified time of a CSV file."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    return "Never"


# =============================================================================
# DEFAULT DATA (fallback if no CSV exists)
# =============================================================================

def get_default_gdp_data() -> pd.DataFrame:
    return pd.DataFrame({
        'Quarter': ['Q1 20', 'Q2 20', 'Q3 20', 'Q4 20', 'Q1 21', 'Q2 21', 'Q3 21', 'Q4 21',
                    'Q1 22', 'Q2 22', 'Q3 22', 'Q4 22', 'Q1 23', 'Q2 23', 'Q3 23', 'Q4 23',
                    'Q1 24', 'Q2 24', 'Q3 24', 'Q4 24', 'Q1 25', 'Q2 25', 'Q3 25'],
        'GDP': [-5.3, -28.0, 34.8, 4.0, 6.3, 7.0, 2.3, 6.9,
                -1.6, -0.6, 3.2, 2.6, 2.2, 2.1, 4.9, 3.4,
                1.4, 3.0, 2.8, 2.3, -0.5, 3.8, 4.3],
        'Disputed': [None]*21 + [1.0, 0.8]
    })


def get_default_sentiment_data() -> pd.DataFrame:
    return pd.DataFrame({
        'Period': ['Jan 19', 'Jul 19', 'Dec 19', 'Jan 20', 'Apr 20', 'Jul 20', 'Dec 20',
                   'Jan 21', 'Jul 21', 'Dec 21', 'Jan 22', 'Jun 22', 'Dec 22',
                   'Jan 23', 'Jul 23', 'Dec 23', 'Jan 24', 'Jul 24', 'Dec 24',
                   'Jan 25', 'Apr 25', 'Jul 25', 'Dec 25'],
        'Michigan': [91.2, 98.4, 99.3, 99.8, 71.8, 72.5, 80.7, 79.0, 81.2, 70.6,
                     67.2, 50.0, 59.7, 64.9, 71.6, 69.7, 79.0, 66.4, 74.0,
                     73.2, 52.2, 61.7, 52.9],
        'Conference Board': [121.7, 135.8, 126.5, 130.4, 85.7, 91.7, 87.1, 87.1, 125.1, 115.2,
                             111.1, 98.7, 109.0, 106.0, 114.0, 108.0, 110.9, 101.9, 104.7,
                             105.3, 86.0, 95.4, 89.1]
    })


def get_default_expectations_data() -> pd.DataFrame:
    return pd.DataFrame({
        'Month': ['Jan 24', 'Feb 24', 'Mar 24', 'Apr 24', 'May 24', 'Jun 24', 'Jul 24', 'Aug 24',
                  'Sep 24', 'Oct 24', 'Nov 24', 'Dec 24', 'Jan 25', 'Feb 25', 'Mar 25', 'Apr 25',
                  'May 25', 'Jun 25', 'Jul 25', 'Aug 25', 'Sep 25', 'Oct 25', 'Nov 25', 'Dec 25'],
        'Value': [83.8, 79.8, 77.4, 68.8, 72.8, 79.0, 82.0, 82.5,
                  82.4, 89.1, 86.0, 78.1, 76.7, 72.9, 65.2, 54.4,
                  72.8, 71.5, 73.4, 75.6, 73.7, 70.7, 70.7, 70.7]
    })


def get_default_unemployment_data() -> pd.DataFrame:
    return pd.DataFrame({
        'Year': ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
        'Overall': [3.5, 8.1, 5.4, 3.6, 3.6, 4.0, 4.6],
        'Young Grads (22-27)': [3.25, 6.5, 5.0, 3.5, 3.8, 4.2, 4.59],
        'Recent Grads': [5.0, 9.0, 7.5, 5.5, 6.0, 7.5, 9.7]
    })


def get_default_housing_data() -> pd.DataFrame:
    return pd.DataFrame({
        'Year': ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
        'Median Price ($K)': [313, 329, 386, 449, 431, 420, 417],
        'Price-to-Income Ratio': [4.1, 4.3, 4.6, 5.2, 5.1, 5.0, 5.0],
        'Cost as % of Income': [35, 37, 40, 48, 47, 47, 47.7],
        'First-Time Buyer Age': [33, 34, 36, 38, 39, 39, 40]
    })


def get_default_vehicle_data() -> pd.DataFrame:
    return pd.DataFrame({
        'Year': ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
        'Avg Transaction Price': [36718, 40107, 47000, 49929, 48528, 47500, 49814],
        'Models Under $25K': [30, 25, 20, 12, 10, 10, 8],
        'Avg Monthly Payment': [554, 575, 641, 717, 726, 734, 754]
    })


# =============================================================================
# DATA LOADING (CSV with fallback to defaults)
# =============================================================================

def load_gdp_data() -> pd.DataFrame:
    df = load_csv("gdp_data.csv")
    return df if df is not None else get_default_gdp_data()


def load_sentiment_data() -> pd.DataFrame:
    df = load_csv("sentiment_data.csv")
    return df if df is not None else get_default_sentiment_data()


def load_expectations_data() -> pd.DataFrame:
    df = load_csv("expectations_data.csv")
    return df if df is not None else get_default_expectations_data()


def load_unemployment_data() -> pd.DataFrame:
    df = load_csv("unemployment_data.csv")
    return df if df is not None else get_default_unemployment_data()


def load_housing_data() -> pd.DataFrame:
    df = load_csv("housing_data.csv")
    return df if df is not None else get_default_housing_data()


def load_vehicle_data() -> pd.DataFrame:
    df = load_csv("vehicle_data.csv")
    return df if df is not None else get_default_vehicle_data()


def load_all_data() -> dict:
    """Load all datasets and return as a dictionary."""
    return {
        'gdp': load_gdp_data(),
        'sentiment': load_sentiment_data(),
        'expectations': load_expectations_data(),
        'unemployment': load_unemployment_data(),
        'housing': load_housing_data(),
        'vehicle': load_vehicle_data()
    }


# =============================================================================
# FRED API FUNCTIONS
# =============================================================================

def fetch_gdp_from_fred(api_key: str) -> pd.DataFrame:
    """
    Fetch quarterly GDP growth rate from FRED.
    Series: A191RL1Q225SBEA (Real GDP, Percent Change from Preceding Period, Quarterly, Seasonally Adjusted Annual Rate)
    """
    if not FRED_AVAILABLE:
        raise ImportError("fredapi not installed")

    fred = Fred(api_key=api_key)

    # Fetch GDP growth rate (annualized quarterly change)
    gdp_series = fred.get_series('A191RL1Q225SBEA', observation_start='2020-01-01')

    # Convert to DataFrame
    df = pd.DataFrame({'date': gdp_series.index, 'GDP': gdp_series.values})

    # Format quarter labels
    def format_quarter(date):
        q = (date.month - 1) // 3 + 1
        return f"Q{q} {str(date.year)[2:]}"

    df['Quarter'] = df['date'].apply(format_quarter)
    df['Disputed'] = None  # Disputed values must be manually entered

    return df[['Quarter', 'GDP', 'Disputed']]


def fetch_unemployment_from_fred(api_key: str) -> pd.DataFrame:
    """
    Fetch unemployment rate from FRED.
    Series: UNRATE (Civilian Unemployment Rate)
    """
    if not FRED_AVAILABLE:
        raise ImportError("fredapi not installed")

    fred = Fred(api_key=api_key)

    # Fetch annual average unemployment (we'll get monthly and average by year)
    unrate = fred.get_series('UNRATE', observation_start='2019-01-01')

    # Convert to DataFrame and calculate annual averages
    df = pd.DataFrame({'date': unrate.index, 'rate': unrate.values})
    df['Year'] = df['date'].dt.year
    annual = df.groupby('Year')['rate'].mean().round(1).reset_index()
    annual.columns = ['Year', 'Overall']
    annual['Year'] = annual['Year'].astype(str)

    # Note: Young Grads and Recent Grads data not available from FRED
    # These would need to be manually updated or sourced elsewhere
    annual['Young Grads (22-27)'] = None
    annual['Recent Grads'] = None

    return annual


def fetch_consumer_sentiment_from_fred(api_key: str) -> pd.DataFrame:
    """
    Fetch University of Michigan Consumer Sentiment from FRED.
    Series: UMCSENT (University of Michigan: Consumer Sentiment)
    """
    if not FRED_AVAILABLE:
        raise ImportError("fredapi not installed")

    fred = Fred(api_key=api_key)

    # Fetch Michigan sentiment
    sentiment = fred.get_series('UMCSENT', observation_start='2019-01-01')

    # Convert to DataFrame
    df = pd.DataFrame({'date': sentiment.index, 'Michigan': sentiment.values})

    # Format period labels
    def format_period(date):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return f"{months[date.month-1]} {str(date.year)[2:]}"

    df['Period'] = df['date'].apply(format_period)

    # Note: Conference Board data not available from FRED (proprietary)
    df['Conference Board'] = None

    return df[['Period', 'Michigan', 'Conference Board']]


# =============================================================================
# BEA API FUNCTIONS
# =============================================================================

def fetch_gdp_from_bea(api_key: str) -> pd.DataFrame:
    """
    Fetch GDP data from Bureau of Economic Analysis API.
    """
    base_url = "https://apps.bea.gov/api/data"

    params = {
        'UserID': api_key,
        'method': 'GetData',
        'datasetname': 'NIPA',
        'TableName': 'T10101',  # Real GDP
        'Frequency': 'Q',
        'Year': ','.join(str(y) for y in range(2020, 2026)),
        'ResultFormat': 'JSON'
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"BEA API error: {response.status_code}")

    data = response.json()

    # Parse the BEA response (structure varies by table)
    # This is a simplified parser - may need adjustment based on actual response
    if 'BEAAPI' in data and 'Results' in data['BEAAPI']:
        results = data['BEAAPI']['Results']
        if 'Data' in results:
            records = results['Data']
            df = pd.DataFrame(records)
            return df

    return None


# =============================================================================
# REFRESH FUNCTIONS
# =============================================================================

def refresh_gdp_data(fred_api_key: str = None, bea_api_key: str = None) -> tuple:
    """
    Refresh GDP data from APIs.
    Returns (success: bool, message: str, data: DataFrame or None)
    """
    try:
        if fred_api_key and FRED_AVAILABLE:
            df = fetch_gdp_from_fred(fred_api_key)

            # Preserve disputed values from existing data
            existing = load_csv("gdp_data.csv")
            if existing is not None and 'Disputed' in existing.columns:
                disputed_map = dict(zip(existing['Quarter'], existing['Disputed']))
                df['Disputed'] = df['Quarter'].map(disputed_map)

            save_csv(df, "gdp_data.csv")
            return True, f"GDP data refreshed ({len(df)} quarters)", df
        else:
            return False, "FRED API key not provided or fredapi not installed", None
    except Exception as e:
        return False, f"Error refreshing GDP: {str(e)}", None


def refresh_unemployment_data(fred_api_key: str = None) -> tuple:
    """
    Refresh unemployment data from FRED.
    Returns (success: bool, message: str, data: DataFrame or None)
    """
    try:
        if fred_api_key and FRED_AVAILABLE:
            df = fetch_unemployment_from_fred(fred_api_key)

            # Preserve grad unemployment from existing data (not in FRED)
            existing = load_csv("unemployment_data.csv")
            if existing is not None:
                grad_map = dict(zip(existing['Year'], existing['Young Grads (22-27)']))
                recent_map = dict(zip(existing['Year'], existing['Recent Grads']))
                df['Young Grads (22-27)'] = df['Year'].map(grad_map)
                df['Recent Grads'] = df['Year'].map(recent_map)

            save_csv(df, "unemployment_data.csv")
            return True, f"Unemployment data refreshed ({len(df)} years)", df
        else:
            return False, "FRED API key not provided or fredapi not installed", None
    except Exception as e:
        return False, f"Error refreshing unemployment: {str(e)}", None


def refresh_sentiment_data(fred_api_key: str = None) -> tuple:
    """
    Refresh consumer sentiment data from FRED.
    Returns (success: bool, message: str, data: DataFrame or None)
    """
    try:
        if fred_api_key and FRED_AVAILABLE:
            df = fetch_consumer_sentiment_from_fred(fred_api_key)

            # Preserve Conference Board data from existing (not in FRED)
            existing = load_csv("sentiment_data.csv")
            if existing is not None:
                cb_map = dict(zip(existing['Period'], existing['Conference Board']))
                df['Conference Board'] = df['Period'].map(cb_map)

            save_csv(df, "sentiment_data.csv")
            return True, f"Sentiment data refreshed ({len(df)} periods)", df
        else:
            return False, "FRED API key not provided or fredapi not installed", None
    except Exception as e:
        return False, f"Error refreshing sentiment: {str(e)}", None


def refresh_all_api_data(fred_api_key: str = None, bea_api_key: str = None) -> dict:
    """
    Refresh all API-available data.
    Returns dict with results for each data type.
    """
    results = {}

    results['gdp'] = refresh_gdp_data(fred_api_key, bea_api_key)
    results['unemployment'] = refresh_unemployment_data(fred_api_key)
    results['sentiment'] = refresh_sentiment_data(fred_api_key)

    # Housing and Vehicle data don't have free APIs - must be manual
    results['housing'] = (False, "Housing data requires manual update (no free API)", None)
    results['vehicle'] = (False, "Vehicle data requires manual update (no free API)", None)

    return results


# =============================================================================
# DATA STATUS
# =============================================================================

def get_data_status() -> dict:
    """Get the status of all data files."""
    files = {
        'GDP': 'gdp_data.csv',
        'Sentiment': 'sentiment_data.csv',
        'Expectations': 'expectations_data.csv',
        'Unemployment': 'unemployment_data.csv',
        'Housing': 'housing_data.csv',
        'Vehicle': 'vehicle_data.csv'
    }

    status = {}
    for name, filename in files.items():
        filepath = DATA_DIR / filename
        if filepath.exists():
            mtime = os.path.getmtime(filepath)
            status[name] = {
                'exists': True,
                'last_updated': datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M"),
                'rows': len(pd.read_csv(filepath))
            }
        else:
            status[name] = {
                'exists': False,
                'last_updated': 'Never',
                'rows': 0
            }

    return status
