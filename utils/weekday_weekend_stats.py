from utils.helper import convert_numpy_type

def get_weekend_weekday_stats(data):
    # Create weekend mask
    weekend_mask = data['Day_of_Week'].isin(['Saturday', 'Sunday'])
    
    # Get weekend data
    weekend_data = data[weekend_mask]
    weekend_avg = convert_numpy_type(weekend_data['Amount'].mean())
    weekend_sum = convert_numpy_type(weekend_data['Amount'].sum())
    weekend_count = convert_numpy_type(len(weekend_data))
    weekend_max = convert_numpy_type(weekend_data['Amount'].max())
    weekend_days = convert_numpy_type(weekend_data['Date'].nunique())
    
    # Get weekday data
    weekday_data = data[~weekend_mask]
    weekday_avg = convert_numpy_type(weekday_data['Amount'].mean())
    weekday_sum = convert_numpy_type(weekday_data['Amount'].sum())
    weekday_count = convert_numpy_type(len(weekday_data))
    weekday_max = convert_numpy_type(weekday_data['Amount'].max())
    weekday_days = convert_numpy_type(weekday_data['Date'].nunique())
    
    # Calculate daily averages
    weekend_daily_avg = convert_numpy_type(weekend_sum / weekend_days) if weekend_days > 0 else 0
    weekday_daily_avg = convert_numpy_type(weekday_sum / weekday_days) if weekday_days > 0 else 0
    
    # Calculate percentage of total
    total_amount = weekend_sum + weekday_sum
    weekend_percentage = convert_numpy_type((weekend_sum / total_amount * 100) if total_amount > 0 else 0)
    weekday_percentage = convert_numpy_type((weekday_sum / total_amount * 100) if total_amount > 0 else 0)
    
    # Prepare comparison dictionary
    time_comparison = {
        "weekend": {
            "total_amount": weekend_sum,
            "transaction_count": weekend_count,
            "average_per_transaction": weekend_avg,
            "average_per_day": weekend_daily_avg,
            "percentage_of_total": weekend_percentage,
            "max_transaction": weekend_max,
            "days_count": weekend_days
        },
        "weekday": {
            "total_amount": weekday_sum,
            "transaction_count": weekday_count,
            "average_per_transaction": weekday_avg,
            "average_per_day": weekday_daily_avg,
            "percentage_of_total": weekday_percentage,
            "max_transaction": weekday_max,
            "days_count": weekday_days
        },
        "comparison": {
            "difference_in_average": abs(weekend_avg - weekday_avg),
            "difference_in_daily_average": abs(weekend_daily_avg - weekday_daily_avg),
            "higher_average_period": "weekend" if weekend_avg > weekday_avg else "weekday",
            "higher_daily_period": "weekend" if weekend_daily_avg > weekday_daily_avg else "weekday",
            "weekend_to_weekday_ratio": convert_numpy_type(weekend_avg / weekday_avg) if weekday_avg > 0 else 0
        }
    }
    
    return time_comparison