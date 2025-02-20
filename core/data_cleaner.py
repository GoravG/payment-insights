import pandas as pd

def clean_data(data):
    """
    Cleans and preprocesses the data.
    Args:
        data (pd.DataFrame): Raw DataFrame.
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    data['Transaction_Date'] = pd.to_datetime(data['Transaction_Date'], errors='coerce')
    data['Amount'] = data['Amount'].astype(float)
    data['Day_of_Week'] = data['Transaction_Date'].dt.day_name()
    data['Hour'] = data['Transaction_Date'].dt.hour
    data['Month'] = data['Transaction_Date'].dt.strftime('%B')
    return data
