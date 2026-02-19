import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
import logging as log
import scripts.pattern as pt 

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        log.warning("normalize_text: input is not a string")
        return None

    text = text.replace("İ", "I").replace("ı", "i")
    text = text.replace("Ö", "O").replace("ö", "o")
    text = text.replace("Ü", "U").replace("ü", "u")
    text = text.replace("Ç", "C").replace("ç", "c")
    text = text.replace("Ş", "S").replace("ş", "s")
    text = text.replace("Ğ", "G").replace("ğ", "g")

    text = text.lower()

    text = re.sub(r"[,\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

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

def remove_features(text):
    if not isinstance(text, str):
        log.warning("remove_features: input is not a string")
        return None
    # removed gpu,series and cpu
    text = normalize_text(text)
    features = get_features(text)

    for feature in features.values():
        if feature:
            text = text.replace(feature, "")
            print(f"Removed feature: {feature}")
            print(f"Text after removal: {text}")
            print("-" * 40)


    return text

def extract_series(text):
    if not isinstance(text, str):
        log.warning("extract_series: input is not a string")
        return None


    match = pt.series_pattern.search(text)
    if match:
        return match.group(0)
    return None

def extract_cpu(text):
    if not isinstance(text, str):
        log.warning("extract_cpu: input is not a string")
        return None

    match = pt.cpu_pattern.search(text)

    if not match:
        return None

    raw = match.group(0)

    raw = raw.replace("-", " ").replace(",", " ").replace("/", " ")
    raw = re.sub(r"\s+", " ", raw).strip()

    raw = re.sub(r"\s+", " ", raw).strip()

    raw = re.sub(r"\br\s*([3579])", r"ryzen \1", raw)

    if re.search(r"\bi[3579]\b", raw):
        if "intel" not in raw:
            raw = "intel core " + raw
    if re.search(r"\bR[3579]?\b", raw):
        if "amd" not in raw:
            raw = "amd " + raw

    raw = raw.title()

    return raw

def extract_gpu(text):
    if not isinstance(text, str):
        log.warning("extract_gpu: input is not a string")
        return None
    match = pt.gpu_pattern.search(text)

    if not match:
        log.info("extract_gpu: no match found in text: %s", text)
        return None

    raw = match.group(0)

    raw = raw.replace("-", " ").replace(",", " ")
    raw=raw.replace("/"," ")
    raw = re.sub(r"\s+", " ", raw).strip()

    raw = re.sub(r"\s+", " ", raw).strip()

    return raw

def extract_ram(text):
    if not isinstance(text, str):
        log.warning("extract_ram: input is not a string")
        return None
    match = pt.ram_pattern.search(text)

    if not match:
        log.info("extract_ram: no match found in text: %s", text)
        return None

    raw = match.group(0)

    raw = raw.replace("-", " ").replace(",", " ")
    raw=raw.replace("/"," ")
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
