import pandas as pd
from utils.helper import to_native
from utils.hourly_stats import get_hourly_stats
from utils.daily_stats import get_daily_stats
from utils.metadata_stats import get_metadata
from utils.monthly_stats import get_monthly_stats
from utils.weekday_weekend_stats import get_weekend_weekday_stats
from utils.overall_stats import get_transaction_insights


def generate_insights_report(data):
    """
    Analyzes the data and generates an insights report in JSON format,
    handling Transaction_Date with surrounding quotes.

    Args:
        data (pd.DataFrame): Cleaned DataFrame with 'Transaction_Date' column.

    Returns:
        dict: Report data in a JSON-serializable format
    """
    # Calculate hourly stats for the filtered data
    report_data = {
        "metadata": get_metadata(data),
        "transaction_insights": get_transaction_insights(data),
        "comparisons": get_weekend_weekday_stats(data),
        "patterns": {
            "daily": get_daily_stats(data),
            "hourly": get_hourly_stats(data),
            "monthly": get_monthly_stats(data),
        },
    }

    return report_data
