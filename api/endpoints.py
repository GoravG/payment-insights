import json
from fastapi import APIRouter, UploadFile
from core.data_loader import load_data
from core.data_cleaner import clean_data
from core.data_analyzer import generate_insights_report
from core.timeseries_converter import convert_timeseries
import numpy as np
import pandas as pd
import os

from utils.helper import to_native

router = APIRouter()


@router.post("/analyze")
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
            data = convert_timeseries(data)
            report = generate_insights_report(data)

            # Convert numpy types to Python native types
            converted_report = to_native({"report": report})

            return converted_report

        finally:
            # Clean up temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}
