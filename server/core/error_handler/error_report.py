import datetime
from typing import Literal
import json
import sys
import os

from core.log.logger import Logger


def generate_error_report(
    error_type: Literal["error", "critical"],
    error_title: str,
    error_description: str,
    error_detail: str,
    time: datetime.datetime,
):
    
    
    error_file = os.path.join(f"data/error_reports/{datetime.datetime.now().strftime("%Y-%m-%d")}.json")

    os.makedirs("data/error_reports", exist_ok=True)
    
    try:
        with open(error_file, 'r', encoding='utf-8') as f:

        
            data = json.load(f)
            
    except json.JSONDecodeError:
            data = []

    except FileNotFoundError:
            data = []




    
    error_report = {
        "id": len(data) + 1,
        "error_info": {
            "type": error_type,
            "title": error_title,
            "description": error_description,
            "detail": error_detail,
            "time": time.isoformat(),
        },
        "sys_info": {
            "os": sys.platform,
            "python": sys.version,  
        }
    }

    data.append(error_report)

    with open(error_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))





    

    

    
