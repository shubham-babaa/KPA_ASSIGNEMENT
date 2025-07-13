# utils/json_utils.py or inline in your API/service file

from datetime import date, datetime

def convert_dates_to_strings(data):
    if isinstance(data, dict):
        return {k: convert_dates_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_dates_to_strings(item) for item in data]
    elif isinstance(data, (date, datetime)):
        return data.isoformat()
    else:
        return data
