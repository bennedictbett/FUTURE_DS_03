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
    df["first_contact_date"] = pd.to_datetime(df["first_contact_date"])
    df["won_date"]           = pd.to_datetime(df["won_date"])
    logging.info(f"Loaded: {df.shape}")
    return df


def calc_channel_metrics(df):
    logging.info("Calculating core channel metrics...")

    channel = df.groupby("origin").agg(
        total_leads         = ("mql_id",    "count"),
        closed_won          = ("converted", "sum"),
        total_revenue       = ("declared_monthly_revenue", "sum"),
        avg_revenue         = ("declared_monthly_revenue", "mean"),
    ).reset_index()

    channel["conversion_rate"] = (
        channel["closed_won"] / channel["total_leads"] * 100
    ).round(2)

    channel["drop_off"] = channel["total_leads"] - channel["closed_won"]

    channel["drop_off_pct"] = (
        channel["drop_off"] / channel["total_leads"] * 100
    ).round(2)

    channel["lead_share_pct"] = (
        channel["total_leads"] / channel["total_leads"].sum() * 100
    ).round(2)

    channel = channel.sort_values("conversion_rate", ascending=False).reset_index(drop=True)

    logging.info(f"\n{channel[['origin','total_leads','closed_won','conversion_rate','drop_off_pct']].to_string(index=False)}")
    return channel


def calc_days_by_channel(df):
    logging.info("Calculating days to close by channel...")

    won_df = df[df["converted"] == 1].copy()

    days = won_df.groupby("origin")["days_to_close"].agg(
        avg_days    = "mean",
        median_days = "median",
        min_days    = "min",
        max_days    = "max",
        count       = "count"
    ).round(1).reset_index()

    days = days.sort_values("median_days").reset_index(drop=True)

    logging.info(f"\n{days.to_string(index=False)}")
    return days


def calc_monthly_by_channel(df):
    logging.info("Calculating monthly trend by channel...")

    monthly = df.groupby(["contact_month", "origin"]).agg(
        total_leads = ("mql_id",    "count"),
        closed_won  = ("converted", "sum")
    ).reset_index()

    monthly["conversion_rate"] = (
        monthly["closed_won"] / monthly["total_leads"] * 100
    ).round(2)

    monthly = monthly.sort_values(["contact_month", "origin"]).reset_index(drop=True)

    logging.info(f"Monthly by channel shape: {monthly.shape}")
    return monthly


def calc_quality_score(channel):
    logging.info("Calculating channel quality scores...")

    
    channel["cvr_score"]    = channel["conversion_rate"] / channel["conversion_rate"].max()
    channel["volume_score"] = channel["total_leads"]     / channel["total_leads"].max()

    
    channel["quality_score"] = (
        (channel["cvr_score"] * 0.6) + (channel["volume_score"] * 0.4)
    ).round(3)

    channel["quality_rank"] = channel["quality_score"].rank(ascending=False).astype(int)

    scored = channel[["origin", "total_leads", "closed_won",
                       "conversion_rate", "quality_score", "quality_rank"]]\
             .sort_values("quality_rank")

    logging.info(f"\n{scored.to_string(index=False)}")
    return channel


def print_summary(channel, days):
    logging.info("── Channel Summary ─────────────────────")

    best_cvr    = channel.iloc[0]
    worst_cvr   = channel.iloc[-1]
    best_vol    = channel.sort_values("total_leads", ascending=False).iloc[0]
    fastest     = days.iloc[0]

    logging.info(f"Best CVR:      {best_cvr['origin']} ({best_cvr['conversion_rate']}%)")
    logging.info(f"Worst CVR:     {worst_cvr['origin']} ({worst_cvr['conversion_rate']}%)")
    logging.info(f"Most leads:    {best_vol['origin']} ({int(best_vol['total_leads']):,})")
    logging.info(f"Fastest close: {fastest['origin']} ({fastest['median_days']} days median)")
    logging.info("────────────────────────────────────────")


def export(channel, days, monthly):
    channel.to_csv(OUTPUT_DIR / "channel_analysis.csv",         index=False)
    days.to_csv(OUTPUT_DIR    / "channel_days_to_close.csv",    index=False)
    monthly.to_csv(OUTPUT_DIR / "channel_monthly_trend.csv",    index=False)

    logging.info(" Exported:")
    logging.info("   - channel_analysis.csv")
    logging.info("   - channel_days_to_close.csv")
    logging.info("   - channel_monthly_trend.csv")


def run():
    df      = load_data()
    channel = calc_channel_metrics(df)
    days    = calc_days_by_channel(df)
    monthly = calc_monthly_by_channel(df)
    channel = calc_quality_score(channel)
    print_summary(channel, days)
    export(channel, days, monthly)
    logging.info(" channel_analysis.py complete")
    return df, channel, days, monthly

if __name__ == "__main__":
    run()