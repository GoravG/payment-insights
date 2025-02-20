import pandas as pd
from utils.helper import convert_numpy_type
from utils.hourly_stats import get_hourly_stats
from utils.daily_stats import get_daily_stats
from utils.weekday_weekend_stats import get_weekend_weekday_stats
from utils.overall_stats import get_overall_stats

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
        "transaction_insights": get_overall_stats(data),
        "daily_patterns": get_daily_stats(data),
        "time_comparison": get_weekend_weekday_stats(data),
        "hourly_transactions": get_hourly_stats(data)
    }
    
    return report_data