import pandas as pd
import json
import numpy as np
from datetime import datetime

def generate_insights_report(data):
    """
    Analyzes the data and generates an insights report in JSON format,
    handling Transaction_Date with surrounding quotes.
    
    Args:
        data (pd.DataFrame): Cleaned DataFrame with 'Transaction_Date' column.
    
    Returns:
        dict: Report data in a JSON-serializable format
    """
    # Helper function to convert numpy types to Python native types
    def convert_numpy_type(obj):
        if isinstance(obj, (np.int8, np.int16, np.int32, np.int64,
                          np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.datetime64):
            return str(obj)
        return obj

    # Clean and convert Transaction_Date
    if 'Transaction_Date' in data.columns:
        # Extract time components
        data['Hour'] = data['Transaction_Date'].dt.hour
        data['Day_of_Week'] = data['Transaction_Date'].dt.day_name()
        data['Month'] = data['Transaction_Date'].dt.strftime('%B')  # Full month name
        data['Month_Num'] = data['Transaction_Date'].dt.month  # For sorting

    filtered_data = data[(data['Hour'] >= 00) & (data['Hour'] <= 24)]
    hourly_stats = filtered_data.groupby('Hour')['Amount'].agg(['mean', 'count', 'sum']).round(2)

    # Convert hourly_stats to a dictionary
    hourly_transactions = {
        f"{hour:02d}:00": {
            "total_amount": convert_numpy_type(stats['sum']),
            "transaction_count": convert_numpy_type(stats['count']),
            "average_amount": convert_numpy_type(stats['mean'])
        }
        for hour, stats in hourly_stats.iterrows()
    }

    # Rest of the function remains the same as before, just updating timestamp references to Transaction_Date
    total_sales = data['Amount'].agg(['sum'])
    daily_stats = data.groupby('Day_of_Week')['Amount'].agg(['mean', 'count', 'sum']).round(2)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_stats = daily_stats.reindex(day_order)
    daily_stats = daily_stats.sort_values('sum', ascending=False)
    
    daily_patterns = {
        str(day): {
            'total_amount': convert_numpy_type(stats['sum']),
            'transaction_count': convert_numpy_type(stats['count']),
            'average_amount': convert_numpy_type(stats['mean'])
        }
        for day, stats in daily_stats.iterrows()
    }
    
    hourly_stats = data.groupby('Hour')['Amount'].mean().round(2)
    peak_hour = convert_numpy_type(hourly_stats.idxmax())
    # peak_hour = hourly_stats.idxmax()
    lowest_hour = convert_numpy_type(hourly_stats.idxmin())
    
    monthly_data = data.groupby(['Month', 'Month_Num'])['Amount'].sum().round(2)
    monthly_data = monthly_data.reset_index().sort_values('Month_Num')
    monthly_stats = pd.Series(monthly_data['Amount'].values, index=monthly_data['Month'])
    
    peak_month = monthly_stats.idxmax()
    lowest_month = monthly_stats.idxmin()
    peak_month_amount = convert_numpy_type(monthly_stats[peak_month])
    lowest_month_amount = convert_numpy_type(monthly_stats[lowest_month])
    
    min_transaction = convert_numpy_type(data['Amount'].min())
    max_transaction = convert_numpy_type(data['Amount'].max())
    avg_transaction = convert_numpy_type(data['Amount'].mean())
    
    customer_totals = data.groupby('Customer_VPA')['Amount'].sum()
    top_customers = {
        f"customer_{i+1}": convert_numpy_type(amount)
        for i, (customer, amount) in enumerate(customer_totals.nlargest(5).items())
    }
    
    weekend_mask = data['Day_of_Week'].isin(['Saturday', 'Sunday'])
    weekend_avg = convert_numpy_type(data[weekend_mask]['Amount'].mean())
    weekday_avg = convert_numpy_type(data[~weekend_mask]['Amount'].mean())
    
    first_date = data['Transaction_Date'].min()
    last_date = data['Transaction_Date'].max()
    first_month_mask = (data['Transaction_Date'].dt.year == first_date.year) & (data['Transaction_Date'].dt.month == first_date.month)
    last_month_mask = (data['Transaction_Date'].dt.year == last_date.year) & (data['Transaction_Date'].dt.month == last_date.month)
    
    avg_first_month = convert_numpy_type(data[first_month_mask]['Amount'].mean())
    avg_last_month = convert_numpy_type(data[last_month_mask]['Amount'].mean())
    pct_change = convert_numpy_type(((avg_last_month - avg_first_month) / avg_first_month) * 100)

    # Calculate hourly stats for the filtered data
    report_data = {
        "transaction_insights": {
            "highest_transaction": max_transaction,
            "lowest_transaction": min_transaction,
            "average_transaction": avg_transaction,
            "date_range": {
                "start": str(first_date.date()),
                "end": str(last_date.date())
            }
        },
        "daily_patterns": daily_patterns,
        "time_comparison": {
            "weekend_average": weekend_avg,
            "weekday_average": weekday_avg,
            "difference": abs(weekend_avg - weekday_avg),
            "higher_period": "weekend" if weekend_avg > weekday_avg else "weekday"
        },
        "hourly_insights": {
            "peak_hour": peak_hour,
            "peak_hour_formatted": f"{peak_hour:02d}:00",
            "peak_hour_average": convert_numpy_type(hourly_stats[peak_hour]),
            "lowest_hour": lowest_hour,
            "lowest_hour_formatted": f"{lowest_hour:02d}:00",
            "lowest_hour_average": convert_numpy_type(hourly_stats[lowest_hour])
        },
        "monthly_patterns": {
            "peak_month": peak_month,
            "peak_month_amount": peak_month_amount,
            "lowest_month": lowest_month,
            "lowest_month_amount": lowest_month_amount
        },
        "top_customers": top_customers,
        "growth_analysis": {
            "first_month_average": avg_first_month,
            "last_month_average": avg_last_month,
            "growth_percentage": pct_change
        },
        "key_findings": [
            f"{daily_stats.index[0]} is the highest spending day, with average transactions of ₹{convert_numpy_type(daily_stats.iloc[0]['mean']):,.2f}",
            f"Most transactions occur at {peak_hour:02d}:00 hours",
            f"Month {peak_month} showed highest spending activity",
            f"{'Weekend' if weekend_avg > weekday_avg else 'Weekday'} spending is higher than {'weekday' if weekend_avg > weekday_avg else 'weekend'} spending",
            f"Average transaction value has {'increased' if pct_change > 0 else 'decreased'} by {abs(pct_change):,.1f}% from first to last month"
        ],
        "total_sales": total_sales,
        "hourly_transactions": hourly_transactions
    }
    
    return report_data