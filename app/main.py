import os
import sys
from pathlib import Path


def get_file_info(filepath: str) -> dict:
    p = Path(filepath)
    return {
        "exists": p.exists(),
        "platform": sys.platform,
        "separator": os.sep,
    }


print(get_file_info("test.txt"))
