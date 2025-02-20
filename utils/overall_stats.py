from utils.helper import convert_numpy_type

def get_overall_stats(data):
    first_date = data['Transaction_Date'].min()
    last_date = data['Transaction_Date'].max()
    first_month_mask = (data['Transaction_Date'].dt.year == first_date.year) & (data['Transaction_Date'].dt.month == first_date.month)
    last_month_mask = (data['Transaction_Date'].dt.year == last_date.year) & (data['Transaction_Date'].dt.month == last_date.month)
    
    avg_first_month = convert_numpy_type(data[first_month_mask]['Amount'].mean())
    avg_last_month = convert_numpy_type(data[last_month_mask]['Amount'].mean())
    pct_change = convert_numpy_type(((avg_last_month - avg_first_month) / avg_first_month) * 100)
    min_transaction = convert_numpy_type(data['Amount'].min())
    max_transaction = convert_numpy_type(data['Amount'].max())
    avg_transaction = convert_numpy_type(data['Amount'].mean())
    total_sales = data['Amount'].agg(['sum'])

    overall_stats = {
            "highest_transaction": max_transaction,
            "lowest_transaction": min_transaction,
            "average_transaction": avg_transaction,
            "date_range": {
                "start": str(first_date.date()),
                "end": str(last_date.date())
            },
            "total_sales": total_sales,
            "growth_analysis": {
            "first_month_average": avg_first_month,
            "last_month_average": avg_last_month,
            "growth_percentage": pct_change
        }
    }
    return overall_stats