import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')


RAW_LEADS  = Path("data/raw/olist_marketing_qualified_leads_dataset.csv")
RAW_DEALS  = Path("data/raw/olist_closed_deals_dataset.csv")
OUTPUT     = Path("data/processed/funnel_clean.csv")


def load_data():
    logging.info("Loading raw data...")
    leads = pd.read_csv(RAW_LEADS)
    deals = pd.read_csv(RAW_DEALS)
    logging.info(f"Leads: {leads.shape} | Deals: {deals.shape}")
    return leads, deals


def merge_data(leads, deals):
    logging.info("Merging leads and deals on mql_id...")
    df = pd.merge(leads, deals, on="mql_id", how="left")
    logging.info(f"Merged shape: {df.shape}")
    return df


def drop_columns(df):
    cols_to_drop = [
        "has_company",
        "has_gtin",
        "average_stock",
        "declared_product_catalog_size",
    ]
    df = df.drop(columns=cols_to_drop)
    logging.info(f"Dropped {len(cols_to_drop)} near-empty columns")
    return df


def fix_missing(df):
    
    df["origin"] = df["origin"].fillna("Unknown")
    df["origin"] = df["origin"].str.strip().str.lower()
    logging.info("Filled 60 missing origins with 'Unknown'")
    return df


def fix_dates(df):
    df["first_contact_date"] = pd.to_datetime(df["first_contact_date"])
    df["won_date"]           = pd.to_datetime(df["won_date"])
    logging.info("Converted date columns to datetime")
    return df


def remove_anomalies(df):
    
    before = len(df)
    df["days_to_close"] = (df["won_date"] - df["first_contact_date"]).dt.days
    df = df[~((df["days_to_close"] < 0))]
    removed = before - len(df)
    logging.info(f"Removed {removed} record(s) with negative days to close")
    return df


def add_features(df):
    
    df["converted"] = df["seller_id"].notnull().astype(int)

    df["contact_month"] = df["first_contact_date"].dt.to_period("M").astype(str)

    df["contact_year"] = df["first_contact_date"].dt.year

    logging.info("Added converted flag, contact_month, contact_year")
    return df


def validate(df):
    logging.info("── Validation ──────────────────────────")
    logging.info(f"Final shape:       {df.shape}")
    logging.info(f"Total leads:       {len(df):,}")
    logging.info(f"Closed won:        {df['converted'].sum():,}")
    logging.info(f"Overall CVR:       {df['converted'].mean()*100:.2f}%")
    logging.info(f"Missing origins:   {df['origin'].isnull().sum()}")
    logging.info(f"Negative days:     {(df['days_to_close'] < 0).sum()}")
    logging.info("────────────────────────────────────────")


def run():
    leads, deals  = load_data()
    df            = merge_data(leads, deals)
    df            = drop_columns(df)
    df            = fix_missing(df)
    df            = fix_dates(df)
    df            = remove_anomalies(df)
    df            = add_features(df)
    validate(df)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    logging.info(f" Clean data saved to {OUTPUT}")
    return df

if __name__ == "__main__":
    run()