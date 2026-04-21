from fileinput import filename
import os

import regex as re
import logging as log
from datetime import datetime
import numpy as np

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        log.warning("utils.normalize_text: input is not a string")
        logging_file("utils_warnings")
        return None

    text = text.replace("İ", "I").replace("ı", "i")
    text = text.replace("Ö", "O").replace("ö", "o")
    text = text.replace("Ü", "U").replace("ü", "u")
    text = text.replace("Ç", "C").replace("ç", "c")
    text = text.replace("Ş", "S").replace("ş", "s")
    text = text.replace("Ğ", "G").replace("ğ", "g")

    text = text.lower()
    logging_file("utils_info")

    text = re.sub(r"[,\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def logging_file(filename: str):
    if not os.path.exists("logs"):
        try:
            os.makedirs("logs")
        except Exception as e:
            print(f"Error creating log directory: {e}")

        try:
            log_file = f"logs/{filename}_{datetime.date()}.log"
            with open(log_file, 'w') as f:
                f.write(f"{filename} log initialized.\n")
            
        except Exception as e:
            print(f"Error initializing log file {filename}: {e}")

        log.basicConfig(
                filename="logs/"+filename+".log",
                level=log.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filemode='w'
            )