# data_init.py
import pandas as pd

from core.anomaly_remover import remove_anamolies

def clean_data(data):
    """
    Cleans and preprocesses the data.
    Args:
        data (pd.DataFrame): Raw DataFrame.
    Returns:
        pd.DataFrame: Cleaned DataFrame with all necessary date fields.
    """
    data = remove_anamolies(data)
    # Convert date and amount fields
    data['Transaction_Date'] = pd.to_datetime(data['Transaction_Date'], errors='coerce')
    data['Amount'] = data['Amount'].astype(float)
    
    # Extract all date components we need
    data['Day_of_Week'] = data['Transaction_Date'].dt.day_name()
    data['Hour'] = data['Transaction_Date'].dt.hour
    data['Month'] = data['Transaction_Date'].dt.strftime('%b')  # Short month name (Jan, Feb, etc.)
    data['Month_Full'] = data['Transaction_Date'].dt.strftime('%B')  # Full month name
    data['Month_Num'] = data['Transaction_Date'].dt.month
    data['Year'] = data['Transaction_Date'].dt.year.astype(str)
    data['Day'] = data['Transaction_Date'].dt.day
    
    # Handle any missing values
    data = data.dropna(subset=['Transaction_Date', 'Amount'])
    
    return data