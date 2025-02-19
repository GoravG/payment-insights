import pandas as pd

def remove_anamolies(data):
    # Remove anomalies (top 1% and bottom 1% of Amount)
    lower_bound = data['Amount'].quantile(0.01)
    upper_bound = data['Amount'].quantile(0.99)
    data = data[(data['Amount'] >= lower_bound) & (data['Amount'] <= upper_bound)]
    
    return data