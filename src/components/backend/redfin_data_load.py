import pandas as pd
import os
import time
from sqlalchemy import create_engine, Column, Integer, String, Float, PrimaryKeyConstraint, Date, DateTime
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def remove_duplicates(df):
    df_copy = df.copy()
    df_copy['last_updated'] = pd.to_datetime(df_copy['last_updated'])
    subset = ['period_begin', 'period_end', 'region_type', 'property_type']
    df_copy = df_copy.sort_values('last_updated', ascending=False).drop_duplicates(subset=subset, keep='first')
    df_copy['last_updated'] = df_copy['last_updated'].astype(str)
    return df_copy


def main():
    print("Establishing connection to the database...")
    engine = create_engine(DATABASE_URL)
    print("Connected to the database!")

    Base = declarative_base()

    class MarketTracker(Base):
        __tablename__ = "market_tracker"
        period_begin = Column(Date)
        period_end = Column(Date)
        period_duration = Column(Integer)
        region_type = Column(String)
        region_type_id = Column(Integer)
        table_id = Column(Integer)
        is_seasonally_adjusted = Column(String)
        region = Column(String)
        city = Column(String)
        state = Column(String)
        state_code = Column(String)
        property_type = Column(String)
        property_type_id = Column(Integer)
        median_sale_price = Column(Float)
        median_sale_price_mom = Column(Float)
        median_sale_price_yoy = Column(Float)
        median_list_price = Column(Float)
        median_list_price_mom = Column(Float)
        median_list_price_yoy = Column(Float)
        median_ppsf = Column(Float)
        median_ppsf_mom = Column(Float)
        median_ppsf_yoy = Column(Float)
        median_list_ppsf = Column(Float)
        median_list_ppsf_mom = Column(Float)
        median_list_ppsf_yoy = Column(Float)
        homes_sold = Column(Float)
        homes_sold_mom = Column(Float)
        homes_sold_yoy = Column(Float)
        pending_sales = Column(Float)
        pending_sales_mom = Column(Float)
        pending_sales_yoy = Column(Float)
        new_listings = Column(Float)
        new_listings_mom = Column(Float)
        new_listings_yoy = Column(Float)
        inventory = Column(Float)
        inventory_mom = Column(Float)
        inventory_yoy = Column(Float)
        months_of_supply = Column(Float)
        months_of_supply_mom = Column(Float)
        months_of_supply_yoy = Column(Float)
        median_dom = Column(Float)
        median_dom_mom = Column(Float)
        median_dom_yoy = Column(Float)
        avg_sale_to_list = Column(Float)
        avg_sale_to_list_mom = Column(Float)
        avg_sale_to_list_yoy = Column(Float)
        sold_above_list = Column(Float)
        sold_above_list_mom = Column(Float)
        sold_above_list_yoy = Column(Float)
        price_drops = Column(Float)
        price_drops_mom = Column(Float)
        price_drops_yoy = Column(Float)
        off_market_in_two_weeks = Column(Float)
        off_market_in_two_weeks_mom = Column(Float)
        off_market_in_two_weeks_yoy = Column(Float)
        parent_metro_region = Column(String)
        parent_metro_region_metro_code = Column(Integer)
        last_updated = Column(DateTime)

        # Define the composite primary key
        __table_args__ = (
            PrimaryKeyConstraint('period_begin', 'period_end', 'region_type', 'region', 'property_type'),
        )

    Base.metadata.create_all(engine)

    dataset_files = [
        'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/redfin_metro_market_tracker.tsv000.gz',
        'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/state_market_tracker.tsv000.gz',
        'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz'
    ]

    # Ensure all datasets have the same columns
    column_set = None
    for dataset_url in dataset_files:
        df = pd.read_csv(dataset_url, sep='\t')
        if column_set is None:
            column_set = set(df.columns)
        elif column_set != set(df.columns):
            raise ValueError("All datasets must have the same columns. Mismatch found!")

    # Load data from URLs into PostgreSQL using pandas and SQLAlchemy
    for dataset_url in dataset_files:
        print(f"Loading data from {dataset_url}...")
        start_time = time.time()
        df = pd.read_csv(dataset_url, sep='\t')
        if "us_national_market_tracker" in dataset_url:
            df = remove_duplicates(df)
        df.to_sql("market_tracker", engine, if_exists='replace', index=False)
        end_time = time.time()
        print(f"Loaded data from {dataset_url} in {end_time - start_time:.2f} seconds.")

    print("Data loaded successfully into PostgreSQL!")


if __name__ == "__main__":
    main()