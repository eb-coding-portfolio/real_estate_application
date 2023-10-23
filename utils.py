import pandas as pd
import os
from pmdarima import auto_arima
from pmdarima.model_selection import train_test_split
from sqlalchemy import create_engine
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from config import table_columns, cohort_raw
import numpy as np
import time


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


def calculate_differences(state_code, property_type, compare_to, sql_engine):
    metric_list = [column for column in table_columns if 'yoy' in column]

    # Get max date across all levels (metro, state, national) from database
    get_max_date = pd.read_sql('select MAX(period_end) as max_date from market_tracker', sql_engine)
    max_date = get_max_date.iloc[0, 0]

    # Step 1: Filter the dataframe by max_date and property_type
    prop_and_date_query = f"select * from market_tracker where property_type = '{property_type}' AND period_end = '{max_date}'"
    # print(prop_and_date_query)
    df = pd.read_sql(prop_and_date_query, sql_engine)
    df.to_csv(r'C:\Users\Eric C. Balduf\Documents\df.csv')

    # Step 2: Further filter by state_code and region_type
    filtered_df = df[
        ((df['region_type'].isin(['metro', 'state']) &
          (df['state_code'] == state_code)) |
         (df['region_type'] == 'national'))
    ]
    filtered_df.to_csv(r'C:\Users\Eric C. Balduf\Documents\filtered_df.csv')

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


def line_chart_predict(line_metric, line_metro, line_prop_type, line_engine, years_before_max=5):
    print("Starting the line_chart_predict function.")

    query = f"""
    SELECT period_end, {line_metric}
    FROM market_tracker 
    where region_type = 'metro' 
    and region =  '{line_metro}'
    and property_type = '{line_prop_type}'
    """

    start_time = time.time()
    result = pd.read_sql(query, line_engine)
    result.to_csv(r'C:\Users\Eric C. Balduf\Documents\result_plot_result.csv', index=False)
    print(result)
    print(f"Data fetched in {time.time() - start_time:.2f} seconds.")

    start_time = time.time()
    result['period_end'] = pd.to_datetime(result['period_end'])
    print(f"Converted 'period_end' to datetime in {time.time() - start_time:.2f} seconds.")

    # Preparing data for ETS
    data = result.set_index('period_end').sort_index()

    print("Fitting the ETS model...")
    start_time = time.time()

    try:
        # Fitting the ETS model using the entire dataset
        model = ExponentialSmoothing(data[line_metric], trend='add', seasonal='add', seasonal_periods=12)
        model_fit = model.fit()

        # Generating a 12-month forecast
        predictions = model_fit.forecast(12)
        predictions.to_csv(r'C:\Users\Eric C. Balduf\Documents\result_plot_predictions.csv', index=False)
        # Calculate the standard error of the residuals
        residuals = data[line_metric] - model_fit.fittedvalues
        std_error = residuals.std()

        # Calculate the upper and lower bounds (90% confidence)
        z_value = 1.645  # 90% confidence
        upper_bound = predictions + (z_value * std_error)
        lower_bound = predictions - (z_value * std_error)

        forecast = pd.DataFrame({
            'period_end': [data.index[-1] + pd.DateOffset(months=i) for i in range(1, 13)],
            line_metric: predictions,
            'upper bound': upper_bound,
            'lower bound': lower_bound
        })

        # Concatenate the original data with the forecast
        plot_df = pd.concat([data, forecast.set_index('period_end')])
        # Filter the output based on years_before_max
        max_date = plot_df.index.max()
        start_date = max_date - pd.DateOffset(years=years_before_max)
        output = plot_df[plot_df.index >= start_date]

        print(f"ETS model fitted and predictions generated in {time.time() - start_time:.2f} seconds.")

        return output.reset_index().rename(columns={"index": "Date"})

    except Exception as e:
        print(f"Error encountered while processing metric {line_metric}: {e}")
        return None


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
            percentage_text = f"{value * 100:.1f}%" if not np.isnan(value) else ""
            bolded_text = f"<b>{percentage_text}</b>"  # Wrap with HTML bold tags

            annotations.append(
                dict(
                    x=x,
                    y=y,
                    xref='x',
                    yref='y',
                    text=bolded_text,
                    showarrow=False,
                    font=dict(
                        family="Arial",
                        size=9,
                        color="black",
                    )
                )
            )
    fig.update_layout(annotations=annotations)
    return fig


if __name__ == "__main__":
    DATABASE_URL = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
    engine = create_engine(DATABASE_URL)
    #prd_line = line_chart_predict('inventory', 'August, ME metro area', 'All Residential', engine)
    #prd_line.to_csv(r'C:\Users\Eric C. Balduf\Documents\result_plot_func_holtw.csv', index=False)
    #
    # engine = create_engine(DATABASE_URL)
    #
    # query = """
    # SELECT period_end, region, property_type, median_sale_price, median_list_price, homes_sold, inventory, avg_sale_to_list
    # FROM market_tracker
    # where region_type = 'metro'
    # """

    # prd_line = line_chart_predict(selected_metric, metro, prop_type, engine)
    # prd_line.to_csv(r'C:\Users\Eric C. Balduf\Documents\result_plot_func.csv', index=False)

    # conn = sqlite3.connect('market_tracker.db')
    # cursor = conn.cursor()
    # query = f"SELECT * FROM {l.table_names['metro']}"
    # data = pd.read_sql_query(query, conn)
    # print(get_stat_val(data, 'period_end', 'max'))
