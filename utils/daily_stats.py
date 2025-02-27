from utils.helper import convert_numpy_type
import pandas as pd

def get_daily_stats(data):
    # First, we need to group by both date and day of week to get daily totals
    data['Date'] = data['Transaction_Date'].dt.date
    daily_totals = data.groupby(['Date', 'Day_of_Week'])['Amount'].sum().reset_index()
    
    # Now we can calculate the average total sum for each day of the week
    day_averages = daily_totals.groupby('Day_of_Week')['Amount'].mean().round(2)
    
    # Original aggregations for other metrics
    daily_stats = data.groupby('Day_of_Week')['Amount'].agg(['mean', 'count', 'sum']).round(2)
    
    # Combine the day averages with the original stats
    daily_stats['daily_average'] = day_averages
    
    # Set the preferred order of days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_stats = daily_stats.reindex(day_order)
    
    # Sort by the sum for display purposes
    daily_stats = daily_stats.sort_values('sum', ascending=False)
    
    # Create the return dictionary with the new daily average
    daily_patterns = {
        str(day): {
            'total_amount': convert_numpy_type(stats['sum']),
            'transaction_count': convert_numpy_type(stats['count']),
            'average_per_transaction': convert_numpy_type(stats['mean']),
            'average_daily_total': convert_numpy_type(stats['daily_average'])
        }
        for day, stats in daily_stats.iterrows()
    }
    
    return daily_patterns