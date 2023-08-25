import pandas as pd
import requests
import time

# Define the URLs for the datasets
dataset_files = [
    'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/redfin_metro_market_tracker.tsv000.gz',
    'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz',
    'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz'
]


def remove_duplicates(df):
    """Remove duplicates based on a subset of columns and keep the latest data."""
    if 'last_updated' not in df.columns:
        # If 'last_updated' doesn't exist, return the original dataframe without modification
        return df

    df_copy = df.copy()
    df_copy['last_updated'] = pd.to_datetime(df_copy['last_updated'])
    subset = ['period_begin', 'period_end', 'region_type', 'property_type']
    df_copy = df_copy.sort_values('last_updated', ascending=False).drop_duplicates(subset=subset, keep='first')
    df_copy['last_updated'] = df_copy['last_updated'].astype(str)
    return df_copy


if __name__ == "__main__":
    all_dataframes = []

    for dataset_url in dataset_files:
        print(f"Loading data from {dataset_url}...")
        start_time = time.time()
        df = pd.read_csv(dataset_url, sep='\t')
        if "us_national_market_tracker" in dataset_url:
            df = remove_duplicates(df)
        all_dataframes.append(df)
        end_time = time.time()
        print(f"Loaded data from {dataset_url} in {end_time - start_time:.2f} seconds.")

    combined_df = pd.concat(all_dataframes, ignore_index=True)
    print(f"Total number of rows after preprocessing: {len(combined_df)}")