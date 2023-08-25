import pandas as pd
import sqlite3
from config import column_definitions

dataset_files = [
    'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/redfin_metro_market_tracker.tsv000.gz',
    'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz',
    'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz'
]

table_names = {
    'metro': 'redfin_metro_market_tracker',
    'state': 'redfin_state_market_tracker',
    'national': 'redfin_us_market_tracker'
}


def read_datasets(files):
    datasets = []
    column_names = None

    for file in files:
        dataset = pd.read_csv(file, delimiter='\t')
        datasets.append(dataset)

    combined_dataset = pd.concat(datasets, ignore_index=True)
    return combined_dataset


def create_database(database_name):
    conn = sqlite3.connect(database_name)
    return conn


def create_table(conn, table_name):
    conn.execute(f'DROP TABLE IF EXISTS {table_name}')

    column_definitions_str = ', '.join([f'{column} {column_definitions[column]}' for column in column_definitions])

    query = f'CREATE TABLE {table_name} ({column_definitions_str})'
    conn.commit()
    conn.execute(query)


def load_data(conn, table_name, dataset):
    columns = ', '.join(dataset.columns)
    placeholders = ', '.join(['?' for _ in dataset.columns])
    query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    conn.executemany(query, dataset.values.tolist())
    conn.commit()  ##added on 7.30.2023


def test_queries(conn, name):
    # Create a cursor object
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(f'SELECT count(*) as row_count_{name} FROM {name}')
    rows = cursor.fetchall()
    cursor.close()
    return rows


def remove_duplicates(df):
    df_copy = df.copy()
    df_copy['last_updated'] = pd.to_datetime(df_copy['last_updated'])

    # Define the subset of columns to identify duplicates
    subset = ['period_begin', 'period_end', 'region_type', 'property_type']

    # Sort by 'last_updated' so the latest date is first, then drop duplicates and keep the first row
    df_copy = df_copy.sort_values('last_updated', ascending=False).drop_duplicates(subset=subset, keep='first')

    # Convert 'last_updated' back to string
    df_copy['last_updated'] = df_copy['last_updated'].astype(str)

    return df_copy


def main():
    dataset = read_datasets(dataset_files)
    conn = create_database('market_tracker.db')

    for region_type, table_name in table_names.items():
        region_data = dataset[dataset['region_type'] == region_type]
        # If region_type is 'national', remove duplicates
        if region_type == 'national':
            region_data = remove_duplicates(region_data)
        print(f"Number of rows for {region_type}: {len(region_data)}")
        create_table(conn, table_name)
        load_data(conn, table_name, region_data)

    for table in list(table_names.values()):
        results = test_queries(conn, table)
        print(results)

    conn.close()


if __name__ == '__main__':
    main()

    # Define a test for removing duplicates from the the naitonal file 
    # url = 'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz'
    #
    # # Read the dataset into a pandas DataFrame
    # df = pd.read_csv(url, sep='\t')
    #
    # # Define the subset of columns to identify duplicates
    # subset = ['period_begin', 'period_end', 'region_type', 'property_type']
    #
    # # Create a new DataFrame that contains only the duplicate rows
    # duplicates = df[df.duplicated(subset=subset, keep=False)]
    #
    # # Print the number of duplicate rows
    # print("Number of duplicate rows:", len(duplicates))
    #
    # # Show the duplicate rows
    # duplicates.sort_values(by=subset)
