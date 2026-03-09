import pandas as pd
from pathlib import Path
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

sys.path.append(os.path.dirname(__file__))

from load_clean       import run as run_load_clean
from funnel_metrics   import run as run_funnel_metrics
from channel_analysis import run as run_channel_analysis

OUTPUT_DIR = Path("data/processed")


def export_summary(df):
    logging.info("Building summary KPIs...")

    summary = {
        "total_leads"         : len(df),
        "closed_won"          : int(df["converted"].sum()),
        "overall_cvr_pct"     : round(df["converted"].mean() * 100, 2),
        "drop_off"            : int((df["converted"] == 0).sum()),
        "avg_days_to_close"   : round(df[df["converted"]==1]["days_to_close"].mean(), 1),
        "median_days_to_close": df[df["converted"]==1]["days_to_close"].median(),
        "best_channel"        : df.groupby("origin")["converted"].mean().idxmax(),
        "worst_channel"       : df.groupby("origin")["converted"].mean().idxmin(),
        "best_month"          : df.groupby("contact_month")["converted"].mean().idxmax(),
        "data_start"          : str(df["first_contact_date"].min().date()),
        "data_end"            : str(df["first_contact_date"].max().date()),
    }

    summary_df = pd.DataFrame([summary]).T.reset_index()
    summary_df.columns = ["metric", "value"]
    summary_df.to_csv(OUTPUT_DIR / "summary_kpis.csv", index=False)

    logging.info(f"\n{summary_df.to_string(index=False)}")
    logging.info("Saved: summary_kpis.csv")
    return summary_df


def print_manifest():
    files = sorted(OUTPUT_DIR.glob("*.csv"))
    logging.info("Output files ready for Power BI:")
    for f in files:
        size_kb = round(f.stat().st_size / 1024, 1)
        logging.info(f"  {f.name:<42} {size_kb} KB")
    logging.info(f"  Total: {len(files)} files")


def run():
    logging.info("Starting full pipeline...")

    logging.info("Step 1 — Load and clean")
    df = run_load_clean()

    logging.info("Step 2 — Funnel metrics")
    df, funnel, monthly, origin, yearly, cycle = run_funnel_metrics()

    logging.info("Step 3 — Channel analysis")
    df, channel, days, monthly_channel = run_channel_analysis()

    logging.info("Step 4 — Summary KPIs")
    export_summary(df)

    logging.info("Step 5 — File manifest")
    print_manifest()

    logging.info("Pipeline complete. Import data/processed/ into Power BI.")


if __name__ == "__main__":
    run()