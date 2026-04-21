import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import regex as re
import logging as log
import scripts.older_pattern as pt
from scripts.utils import gpu_utils ,cpu_utils
from scripts.utils.utils import normalize_text
import scripts.utils.utils as utils
import numpy as np

def get_features(text)-> dict:
    if not isinstance(text, str):
        log.warning("get_features: input is not a string")
        return None

    text = normalize_text(text)

    cpu = extract_cpu(text)
    gpu = extract_gpu(text)
    series = extract_series(text)
    ram = extract_ram(text)
    os = extract_os(text)

    return {
        "cpu": cpu,
        "gpu": gpu,
        "series": series,
        "ram": ram,
        "os": os
    }


    
def extract_cpu(text):
    if not isinstance(text, str):
        log.warning("extract_cpu: input is not a string")
        utils.logging_file("cpu_warnings")
        return None

    return cpu_utils.handle_cpu(text)

def extract_gpu(text):
    if not isinstance(text, str):
        log.warning("extract_gpu: input is not a string")
        utils.logging_file("gpu_warnings")
        return None

    return gpu_utils.handle_gpu(text)



def extract_ram(text):    
    return None

def extract_os(text):
    return None

def extract_storage(text):
    return None

def extract_series(text):
    return None