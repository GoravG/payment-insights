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
    # For future use
    return data