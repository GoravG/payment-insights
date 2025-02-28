def get_metadata(data):
    return {
        "date_range": {
            "start": data["Transaction_Date"].min(),
            "end": data["Transaction_Date"].max(),
        }
    }
