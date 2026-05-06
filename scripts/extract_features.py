import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import logging as log
from scripts.utils import gpu_utils ,cpu_utils, os_utils, ram_utils, storage_utils
from scripts.utils.utils import normalize_text
import scripts.utils.utils as utils
from concurrent.futures import ThreadPoolExecutor, as_completed

def thread_extract_features(key,func, text):
    try:
        result = func(text)
        return key, result
    except Exception as e:
        log.error(f"Error in thread_extract_features for {key}: {e}")
        utils.logging_file(f"{key}_errors", str(e))
        return key, None

def get_features_parallel(text) -> dict:
    if not isinstance(text,str):
        log.warning("get_features_parallel: input is not a string")
        return None
    text = utils.normalize_text(text)

    extractors={
        "cpu": extract_cpu,
        "gpu": extract_gpu,
        "storage": extract_storage,
        "ram": extract_ram,
        "os": extract_os
    }
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures={
            key: executor.submit(thread_extract_features, key,func,text)
            for key, func in extractors.items()
        }
        result={}
        for key,fut in futures.items():
            try:
                _,value=fut.result(timeout=10)
                result[key]=value
            except TimeoutError:
                log.error(f"Timeout while getting result for {key}")
                utils.logging_file(f"{key}_errors", "TimeoutError")
                result[key]=None
            except Exception as e:
                log.error(f"Error getting result for {key}: {e}")
                utils.logging_file(f"{key}_errors :{ str(e)}")
                result[key]=None
        return result

def get_features(text)-> dict:
    if not isinstance(text, str):
        log.warning("get_features: input is not a string")
        return None

    text = normalize_text(text)

    cpu = extract_cpu(text)
    gpu = extract_gpu(text)
    storage= extract_storage(text)
    ram = extract_ram(text)
    os = extract_os(text)

    return {
        "cpu": cpu,
        "gpu": gpu,
        "storage": storage,
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
    if not isinstance(text, str):
        log.warning("extract_ram: input is not a string")
        utils.logging_file("ram_warnings")
        return None
    return ram_utils.handle_ram(text)

def extract_storage(text):
    if not isinstance(text, str):
        log.warning("extract_storage: input is not a string")
        utils.logging_file("storage_warnings")
        return None
    return storage_utils.handle_storage(text)

def extract_os(text):
    if not isinstance(text, str):
        log.warning("extract_os: input is not a string")
        utils.logging_file("os_warnings")
        return None
    return os_utils.handle_os(text)

