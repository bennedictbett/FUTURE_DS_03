import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

CLEAN_DATA = Path("data/processed/funnel_clean.csv")
OUTPUT_DIR = Path("data/processed")


def load_data():
    logging.info("Loading clean data...")
    df = pd.read_csv(CLEAN_DATA)
    logging.info(f"Loaded: {df.shape}")
    return df


def calc_funnel_metrics(df):
    logging.info("Calculating funnel metrics...")

    total_leads  = len(df)
    closed_won   = df["converted"].sum()
    not_converted = total_leads - closed_won

    funnel = pd.DataFrame([
        {
            "stage"           : "Leads",
            "count"           : total_leads,
            "converted_from"  : None,
            "conversion_rate" : 100.0,
            "drop_off"        : 0,
            "drop_off_pct"    : 0.0,
        },
        {
            "stage"           : "Closed Won",
            "count"           : closed_won,
            "converted_from"  : total_leads,
            "conversion_rate" : round(closed_won / total_leads * 100, 2),
            "drop_off"        : not_converted,
            "drop_off_pct"    : round(not_converted / total_leads * 100, 2),
        }
    ])

    logging.info(f"\n{funnel.to_string(index=False)}")
    return funnel


def calc_monthly_trend(df):
    logging.info("Calculating monthly trend...")

    monthly = df.groupby("contact_month").agg(
        total_leads  = ("mql_id",    "count"),
        closed_won   = ("converted", "sum")
    ).reset_index()

    monthly["conversion_rate"] = (
        monthly["closed_won"] / monthly["total_leads"] * 100
    ).round(2)

    monthly["drop_off"] = monthly["total_leads"] - monthly["closed_won"]

    
    monthly = monthly.sort_values("contact_month").reset_index(drop=True)

    
    monthly["cvr_change"] = monthly["conversion_rate"].diff().round(2)

    logging.info(f"\n{monthly.to_string(index=False)}")
    return monthly


def calc_cvr_by_origin(df):
    logging.info("Calculating CVR by origin...")

    origin = df.groupby("origin").agg(
        total_leads = ("mql_id",    "count"),
        closed_won  = ("converted", "sum")
    ).reset_index()

    origin["conversion_rate"] = (
        origin["closed_won"] / origin["total_leads"] * 100
    ).round(2)

    origin["drop_off"] = origin["total_leads"] - origin["closed_won"]

    origin = origin.sort_values("conversion_rate", ascending=False).reset_index(drop=True)

    logging.info(f"\n{origin.to_string(index=False)}")
    return origin


def calc_cvr_by_year(df):
    logging.info("Calculating CVR by year...")

    yearly = df.groupby("contact_year").agg(
        total_leads = ("mql_id",    "count"),
        closed_won  = ("converted", "sum")
    ).reset_index()

    yearly["conversion_rate"] = (
        yearly["closed_won"] / yearly["total_leads"] * 100
    ).round(2)

    logging.info(f"\n{yearly.to_string(index=False)}")
    return yearly


def calc_sales_cycle(df):
    logging.info("Calculating sales cycle...")

    won_df = df[df["converted"] == 1].copy()

    cycle = pd.DataFrame([{
        "metric"  : "mean_days_to_close",
        "value"   : round(won_df["days_to_close"].mean(), 1)
    }, {
        "metric"  : "median_days_to_close",
        "value"   : round(won_df["days_to_close"].median(), 1)
    }, {
        "metric"  : "min_days_to_close",
        "value"   : won_df["days_to_close"].min()
    }, {
        "metric"  : "max_days_to_close",
        "value"   : won_df["days_to_close"].max()
    }, {
        "metric"  : "total_won",
        "value"   : len(won_df)
    }])

    logging.info(f"\n{cycle.to_string(index=False)}")
    return cycle


def export(funnel, monthly, origin, yearly, cycle):
    funnel.to_csv(OUTPUT_DIR / "funnel_metrics.csv",   index=False)
    monthly.to_csv(OUTPUT_DIR / "monthly_trend.csv",   index=False)
    origin.to_csv(OUTPUT_DIR / "cvr_by_origin.csv",    index=False)
    yearly.to_csv(OUTPUT_DIR / "cvr_by_year.csv",      index=False)
    cycle.to_csv(OUTPUT_DIR / "sales_cycle.csv",       index=False)

    logging.info("  Exported:")
    logging.info("   - funnel_metrics.csv")
    logging.info("   - monthly_trend.csv")
    logging.info("   - cvr_by_origin.csv")
    logging.info("   - cvr_by_year.csv")
    logging.info("   - sales_cycle.csv")


def run():
    df      = load_data()
    funnel  = calc_funnel_metrics(df)
    monthly = calc_monthly_trend(df)
    origin  = calc_cvr_by_origin(df)
    yearly  = calc_cvr_by_year(df)
    cycle   = calc_sales_cycle(df)
    export(funnel, monthly, origin, yearly, cycle)
    logging.info(" funnel_metrics.py complete")
    return df, funnel, monthly, origin, yearly, cycle

if __name__ == "__main__":
    run()