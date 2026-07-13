import datetime
from os import error
from typing import Literal
import json
from core.log.logger import Logger
import uuid
import sys
import os

def generate_error_report(
    error_type: Literal["error", "critical"],
    error_title: str,
    error_description: str,
    error_detail: str,
    time: datetime.datetime,
):
    
    error_id = str(uuid.uuid4())

    error_report = {
        "id": error_id,
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

    import extensions
    if hasattr(extensions, 'logger')  and isinstance(extensions.logger, Logger):
        extensions.logger.info(
            f"Generated error report: {error_id}",
            class_name="ERROR_HANDLER",
            method="GeneratedErrorReport",
        )
    else:
        print(f"Generated error report: {error_id}")

    if not os.path.exists("data/error_reports"):
        os.makedirs("data/error_reports")
        
    
    with open(f"data/error_reports/{error_id}.json", "w", encoding="utf-8") as f:
        json.dump(error_report, f, indent=4, ensure_ascii=False)

    

    
