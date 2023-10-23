import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
import os
from sqlalchemy import create_engine
import time
import numpy as np
from config import cohort_raw


def compute_mape(actual, predicted):
    """Compute the Mean Absolute Percentage Error (MAPE)"""
    actual, predicted = np.array(actual), np.array(predicted)

    # Check for zeros in the actual values and handle them appropriately
    if 0 in actual:
        print("Warning: Actual values contain zero(s). MAPE may be inaccurate!")
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100

    # Check for NaN or inf in the result
    if np.isnan(mape) or np.isinf(mape):
        print(f"Warning: Computed MAPE is {mape} for actuals: {actual} and predictions: {predicted}")
        return None
    return mape


def compute_mape_for_hw(data, metric):
    # Splitting the data into train and test
    train, test = data.iloc[:-12], data.iloc[-12:]
    try:
        model = ExponentialSmoothing(train[metric], trend='mul', seasonal='mul', seasonal_periods=12)
        start_time = time.time()
        model_fit = model.fit()
        predictions = model_fit.forecast(len(test))
        mape = compute_mape(test[metric], predictions)
        print(f"Actual values for {metric} in {data['region'].iloc[0]}:\n {test[metric].tolist()}")
        print(f"Predicted values for {metric} in {data['region'].iloc[0]}:\n {predictions.tolist()}")
        print(f"Time taken for fitting and predicting with metric {metric}: {time.time() - start_time:.2f} seconds")
        return mape
    except Exception as e:
        print(f"Error for metric {metric}: {e}")
        return None


if __name__ == "__main__":
    DATABASE_URL = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")

    cohort_df = pd.DataFrame(cohort_raw)
    regions = cohort_df['region'].tolist()

    engine = create_engine(DATABASE_URL)

    placeholders = ', '.join(['%s' for _ in regions])
    query = """
    SELECT period_end, region, property_type, median_sale_price, median_list_price, homes_sold, inventory, avg_sale_to_list
    FROM market_tracker
    where region_type = 'metro'
    AND property_type = 'All Residential'
    AND region in ({})
    """.format(placeholders)

    raw_result = pd.read_sql(query, engine, params=[tuple(regions)])
    raw_result = raw_result.dropna(
        subset=['median_sale_price', 'median_list_price', 'homes_sold', 'inventory', 'avg_sale_to_list'], how='all')

    mape_results = {}

    for region in raw_result['region'].unique():
        print(f"\nProcessing region: {region}")
        region_data = raw_result[raw_result['region'] == region].sort_values(by='period_end')

        for metric in ['median_sale_price', 'median_list_price', 'homes_sold', 'inventory', 'avg_sale_to_list']:
            print(f"  Processing metric: {metric}")
            mape = compute_mape_for_hw(region_data, metric)
            mape_results[(region, metric)] = mape

    mape_df = pd.DataFrame(list(mape_results.items()), columns=['Region_Metric', 'MAPE'])
    mape_df[['region', 'metric']] = pd.DataFrame(mape_df['Region_Metric'].tolist(), index=mape_df.index)
    mape_df.drop('Region_Metric', axis=1, inplace=True)
    mape_df = mape_df[['region', 'metric', 'MAPE']]

    print("\nCompleted processing all regions and metrics.")
    mape_df.to_csv(r'C:\Users\Eric C. Balduf\Documents\holtwinters_mulmul_mape.csv')
