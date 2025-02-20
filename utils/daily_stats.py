from utils.helper import convert_numpy_type

def get_daily_stats(data):
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
    return daily_patterns