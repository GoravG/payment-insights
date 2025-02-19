from fastapi import APIRouter, File, UploadFile
from core.data_loader import load_data
from core.data_cleaner import clean_data
from core.data_analyzer import generate_insights_report
from core.anomaly_remover import remove_anamolies

router = APIRouter()

@router.post("/analyze/")
async def analyze_file(file: UploadFile):
    # Read the uploaded file
    file_content = await file.read()

    # Load and process the data
    with open("temp.csv", "wb") as temp_file:
        temp_file.write(file_content)

    data = load_data("temp.csv")
    data = clean_data(data)
    # data = remove_anamolies(data)
    report = generate_insights_report(data)
    return {"report": report}