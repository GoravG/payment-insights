import pandas as pd
from utils.helper import convert_numpy_type

def get_monthly_stats(data):
    monthly_data = data.groupby(['Month', 'Month_Num'])['Amount'].sum().round(2)
    monthly_data = monthly_data.reset_index().sort_values('Month_Num')
    monthly_stats = pd.Series(monthly_data['Amount'].values, index=monthly_data['Month'])
    
    peak_month = monthly_stats.idxmax()
    lowest_month = monthly_stats.idxmin()
    peak_month_amount = convert_numpy_type(monthly_stats[peak_month])
    lowest_month_amount = convert_numpy_type(monthly_stats[lowest_month])

    monthly_patterns = {
        'peak_month': peak_month,
        'lowest_month': lowest_month,
        'peak_month_amount': peak_month_amount,
        'lowest_month_amount': lowest_month_amount
    }
    return monthly_patterns