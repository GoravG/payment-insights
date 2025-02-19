from core.data_loader import load_data
from core.data_cleaner import clean_data
from core.data_analyzer import generate_insights_report
from fastapi import FastAPI
from api.endpoints import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
