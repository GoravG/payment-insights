import json
from fastapi import APIRouter, UploadFile
from core.data_loader import load_data
from core.data_cleaner import clean_data
from core.data_analyzer import generate_insights_report
from core.transaction_pattern_analyzer import TransactionPatternAnalyzer
import numpy as np
import pandas as pd
import os

router = APIRouter()

def convert_numpy_to_python(obj):
    """
    Recursively converts numpy types to Python native types in a nested structure
    """
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32,
                       np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    elif isinstance(obj, (pd.Series,)):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_to_python(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_python(item) for item in obj]
    return obj

@router.post("/analyze/")
async def analyze_file(file: UploadFile):
    try:
        # Read the uploaded file
        file_content = await file.read()
        
        # Create temp file
        temp_filename = "temp.csv"
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(file_content)
        
        try:
            # Load and process the data
            data = load_data(temp_filename)
            data = clean_data(data)
            report = generate_insights_report(data)
            
            # Convert numpy types to Python native types
            converted_report = convert_numpy_to_python({"report": report})
            
            return converted_report
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}

@router.post("/analyze-transactions/")
async def analyze_transactions_from_file(file: UploadFile):
    try:
        # Get initial report
        initial_report = await analyze_file(file)
        
        if "error" in initial_report:
            return initial_report
        
        # Get analyzer instance and analyze data
        analyzer = TransactionPatternAnalyzer.get_instance()
        analysis_results = analyzer.analyze_new_data(initial_report)
        
        # Convert results to JSON-serializable format
        converted_results = convert_numpy_to_python(analysis_results)
        
        return converted_results
        
    except Exception as e:
        return {"error": f"Error analyzing transactions: {str(e)}"}