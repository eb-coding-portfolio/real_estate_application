import pandas as pd
import sqlite3
from src.components.backend import load_data as ld
from config import table_columns
import numpy as np

def get_stat_val(input_dataframe: pd.DataFrame, column: str, stat: str):
    if column in ('period_end', 'period_begin'):
        input_dataframe[column] = pd.to_datetime(input_dataframe[column])

    column_stats = input_dataframe[column].describe()

    value = column_stats[stat]

    return value


def rank(df: pd.DataFrame, rank_num: int, metric: str):
    df['Rank'] = df[metric].rank(ascending=False)
    df_ranked = df.sort_values(by='Rank', ascending=False)
    top_n = df_ranked.head(rank_num).sort_values(by='Rank', ascending=True)
    bottom_n = df_ranked.tail(rank_num).sort_values(by='Rank', ascending=True)
    df_plot = pd.concat([top_n, bottom_n]).drop_duplicates()
    df_plot = df_plot.sort_values(by='Rank', ascending=False)
    return df_plot


def convert_to_percent(df: pd.DataFrame, column_name: str):
    """
    Convert a column in a DataFrame from decimal to percent.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to convert to percent.

    Returns:
        pd.DataFrame: A new DataFrame with the specified column converted to percent.

    Raises:
        ValueError: If the column_name is not present in the DataFrame or if the column contains non-numeric values.
    """
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    # Check if the column contains numeric values
    if not pd.api.types.is_numeric_dtype(df[column_name]):
        raise ValueError(f"The column '{column_name}' does not contain numeric values.")

    # Multiply the column by 100 to convert from decimal to percent
    converted_df = df.copy()
    converted_df[column_name] *= 100

    return converted_df


def calculate_differences(df, state_code, property_type, compare_to):
    metric_list = [column for column in table_columns if 'yoy' in column]
    # Step 1: Filter the dataframe
    max_date = get_stat_val(df, 'period_end', 'max')
    # Step 1: Filter the dataframe by max_date and property_type
    filtered_df_by_date_and_property = df[
        (df['period_end'] == max_date) &
        (df['property_type'] == property_type)
        ]

    # Step 2: Further filter by state_code and region_type
    filtered_df = filtered_df_by_date_and_property[
        ((filtered_df_by_date_and_property['region_type'].isin(['metro', 'state']) &
          (filtered_df_by_date_and_property['state_code'] == state_code)) |
         (filtered_df_by_date_and_property['region_type'] == 'national'))
    ]
    # Step 2: Determine the reference row
    if compare_to == 'state':
        reference_rows = filtered_df[filtered_df['region_type'] == 'state'].iloc[0]
    else:  # Assuming 'national' is the only other option
        reference_rows = filtered_df[filtered_df['region_type'] == 'national'].iloc[0]

    # Step 3: Calculate the differences
    differences = []
    for _, row in filtered_df.iterrows():
        if row['region_type'] == 'metro':  # We only want to compute differences for metros
            diff_row = {}
            diff_row['region'] = row['region']
            for metric in metric_list:
                diff_row[metric] = row[metric] - reference_rows[metric]
            differences.append(diff_row)

    # Convert differences list of dictionaries to a dataframe
    diff_df = pd.DataFrame(differences)

    # Order the dataframe by 'region' column A-Z
    diff_df = diff_df.sort_values(by='region')

    # Drop rows where all metric columns have NaN values
    diff_df = diff_df.dropna(subset=metric_list, how='all')

    return diff_df


def add_heatmap_annotations(fig, data):
    """
    Adds annotations (text) to the heatmap cells.

    Parameters:
    - fig: The figure object to which annotations are added.
    - data: The data used to generate the heatmap.
    """
    annotations = []
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            value = data.iloc[y, x]
            # Convert the number to a percentage and format it only if the value is not NaN
            percentage_text = f"{value * 100:.2f}%" if not np.isnan(value) else ""

            annotations.append(
                dict(
                    x=x,
                    y=y,
                    xref='x',
                    yref='y',
                    text=percentage_text,
                    showarrow=False,
                    font=dict(
                        family="Arial",
                        size=10,
                        color="black"
                    )
                )
            )
    fig.update_layout(annotations=annotations)
    return fig


if __name__ == "__main__":
    conn = sqlite3.connect('src/components/backend/market_tracker.db')
    cursor = conn.cursor()
    query = f"""

            SELECT * FROM {ld.table_names['metro']}
            UNION ALL 
            SELECT * FROM {ld.table_names['state']}
            UNION ALL 
            SELECT * FROM {ld.table_names['national']}
            
            """
    data = pd.read_sql_query(query, conn)
    state_code = 'TX'
    property_type = 'All Residential'  # replace with the desired property type
    compare_to = 'national'
    result = calculate_differences(data, state_code, property_type, compare_to)
    result.to_csv(r'C:\Users\Eric C. Balduf\Documents\table_test.csv')

    # conn = sqlite3.connect('market_tracker.db')
    # cursor = conn.cursor()
    # query = f"SELECT * FROM {l.table_names['metro']}"
    # data = pd.read_sql_query(query, conn)
    # print(get_stat_val(data, 'period_end', 'max'))
