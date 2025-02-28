import pandas as pd
from utils.helper import to_native
import calendar
from datetime import datetime


def get_monthly_stats(data):
    # Calculate monthly statistics
    monthly_stats = (
        data.groupby(["Month", "Month_Num", "Year"])["Amount"]
        .agg(["mean", "count", "sum"])
        .round(2)
    )

    # Reset index
    monthly_stats = monthly_stats.reset_index()

    # Create date range format for keys
    def create_date_range(row):
        year = int(row["Year"])
        month = int(row["Month_Num"])
        # Get the last day of the month
        last_day = calendar.monthrange(year, month)[1]
        # Format as "1 Jan 2023 - 31 Jan 2023"
        start_date = f"1 {row['Month']} {row['Year']}"
        end_date = f"{last_day} {row['Month']} {row['Year']}"
        return f"{start_date} - {end_date}"

    monthly_stats["date_range"] = monthly_stats.apply(create_date_range, axis=1)

    # Create a proper sort key: year*100 + month for chronological sorting
    monthly_stats["sort_key"] = monthly_stats.apply(
        lambda x: int(x["Year"]) * 100 + int(x["Month_Num"]), axis=1
    )

    # Sort chronologically
    monthly_stats = monthly_stats.sort_values("sort_key")

    # Find peak and lowest months
    peak_month_idx = monthly_stats["sum"].idxmax()
    lowest_month_idx = monthly_stats["sum"].idxmin()

    peak_month = monthly_stats.loc[peak_month_idx, "date_range"]
    lowest_month = monthly_stats.loc[lowest_month_idx, "date_range"]

    # Create combined dictionary with ordered keys
    # We'll use an OrderedDict to ensure the order is preserved
    from collections import OrderedDict

    # First create the sorted list of entries
    sorted_entries = []
    for _, row in monthly_stats.iterrows():
        entry = {
            "date_range": row["date_range"],
            "total_amount": to_native(row["sum"]),
            "transaction_count": to_native(row["count"]),
            "average_amount": to_native(row["mean"]),
            "sort_key": row["sort_key"],
        }
        sorted_entries.append(entry)

    # Create the monthly_transactions dictionary with sorted keys
    monthly_transactions = OrderedDict()
    for entry in sorted_entries:
        monthly_transactions[entry["date_range"]] = {
            "total_amount": entry["total_amount"],
            "transaction_count": entry["transaction_count"],
            "average_amount": entry["average_amount"],
        }

    # Create combined dictionary
    monthly_analysis = {
        "peak_month": peak_month,
        "lowest_month": lowest_month,
        "peak_month_amount": to_native(monthly_stats.loc[peak_month_idx, "sum"]),
        "lowest_month_amount": to_native(monthly_stats.loc[lowest_month_idx, "sum"]),
        "monthly_transactions": monthly_transactions,
    }

    return monthly_analysis
