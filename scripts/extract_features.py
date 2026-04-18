import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import regex as re
import logging as log
import scripts.older_pattern as pt
import scripts.gpu_scripts.gpu_utils as gpu_utils
from scripts.utils import normalize_text


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


def extract_series(text):
    if not isinstance(text, str):
        log.warning("extract_series: input is not a string")
        return None


    match = pt.series_pattern.search(text)
    if match:
        return match.group(0)
    return None


def normalize_cpu(raw: str) -> str:
    raw = raw.replace("-", " ").replace(",", " ").replace("/", " ")
    raw = re.sub(r"\s+", " ", raw).strip()
    raw = re.sub(r"\br\s*([3579])", r"ryzen \1", raw)

    if re.search(r"\bi[3579]\b", raw):
        if "intel" not in raw.lower():
            raw = "intel core " + raw

    if re.search(r"\bR[3579]?\b", raw):
        if "amd" not in raw.lower():
            raw = "amd " + raw

    return raw.title()

def detect_cpu_brand(text:str) -> str:
    model_pattern=re.compile(r"""\b\d{4,5}[a-zA-Z]{0,2}\b""",re.VERBOSE,re.IGNORECASE)

    
    model_match=re.search(model_pattern,text)



    if (model_match.group(0).startswith("i") or model_match.group(0).startswith("u")) or (model_match.group(0).startswith("1")):
        return "intel"
    elif model_match.group(0).startswith("R") or model_match.group(0).startswith(("3","5","7","9")):
        return "amd"
    else:
        return "unknown"
    
def extract_cpu(text):
    if not isinstance(text, str):
        log.warning("extract_cpu: input is not a string")
        return None

    match = pt.cpu_pattern.search(text)

    if not match:
        log.info("extract_cpu: no match found in text: %s", text)
        return None
    raw = match.group(0)
    normalized = normalize_cpu(raw)
    return normalized

def extract_gpu(text):
    if not isinstance(text, str):
        log.warning("extract_gpu: input is not a string")
        return None

    return gpu_utils.handle_gpu(text)



def extract_ram(text):
    if not isinstance(text, str):
        log.warning("extract_ram: input is not a string")
        return None
    
    matchList=pt.ram_pattern.findall(text)

    matchList 


    match = pt.ram_pattern.search(text)

    if not match:
        log.info("extract_ram: no match found in text: %s", text)
        return None



    raw = match.group(0)


    raw = raw.replace("-", " ").replace(",", " ")
    raw=raw.replace("/"," ")
    if re.search(r"\b(\d+)\s*(gb?|tb?)\b|\bddr[3456]", raw, re.IGNORECASE):  
        raw = re.sub(r"\b(\d+)\s*gb\b", r"\1 GB", raw, flags=re.IGNORECASE)
        raw = re.sub(r"\b(\d+)\s*tb\b", r"\1 TB", raw, flags=re.IGNORECASE)
        raw = re.sub(r"\bddr([3456])\s*?(\d+)\b", r"DDR\1 \2 GB", raw, flags=re.IGNORECASE)

    raw = re.sub(r"\s+", " ", raw).strip()
    raw = re.sub(r"(\d+)([a-zA-Z]+)", r"\1 \2", raw)

    raw = re.sub(r"\s+", " ", raw).strip()

    return raw

def extract_os(text):
    if not isinstance(text, str):
        log.warning("extract_os: input is not a string")
        return None
    
    match = pt.os_pattern.search(text)

    if not match:
        log.info("extract_os: no match found in text: %s", text)
        return None

    raw = match.group(0)
    return raw

def extract_storage(text):
    if not isinstance(text, str):
        log.warning("extract_storage: input is not a string")
        return None
    match = pt.stroge_pattern.findall(text)

    if not match:
        log.info("extract_storage: no match found in text: %s", text)
        return None
    max_storage = max(match, key=lambda x: int(x[0]) if x[1].lower() == 'gb' else int(x[0]) * 1024)  


    raw = " ".join(max_storage).strip()


    return raw
