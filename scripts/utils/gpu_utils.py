import scripts.pattern.gpu_pattern as pt
import regex as re
import logging as log
import scripts.utils.utils as utils

import pandas as pd
import numpy as np

def get_gpu_patterns():
    return {
        "amd": pt.amd_gpu_pattern,
        "nvidia": pt.nvidia_gpu_pattern,
        "intel": pt.intel_gpu_pattern,
        "apple": pt.apple_gpu_pattern
    }


def handle_gpu(text):
    if pd.isna(text):
        return None
    
    text = utils.normalize_text(text)

    # 1. NVIDIA
    nv_match = pt.nvidia_gpu_pattern.search(text)
    if nv_match:
        prefix = nv_match.group(1) 
        pro = (nv_match.group(2) or "").replace(" ", "")
        number = nv_match.group(3) 
        suffix = nv_match.group(4) or "" 
        
        if prefix == "mx":
            return f"mx{number}"                     # Örn: mx570a
        if pro == "a":
            return f"rtx a{number}{suffix}"          # Örn: rtx a500
        if pro == "pro":
            return f"{prefix} pro {number}{suffix}"  # Örn: rtx pro 1000
            
        return f"{prefix} {number}{suffix}"          # Örn: rtx 4060, rtx 5070ti

    # 2. AMD
    amd_match = pt.amd_gpu_pattern.search(text)
    if amd_match:
        model = amd_match.group(2)
        if model:
            return f"radeon {model}"                 # Örn: radeon 780m
        return "amd radeon"                          # Örn: amd radeon

    # 3. Intel
    intel_match = pt.intel_gpu_pattern.search(text)
    if intel_match:
        found = intel_match.group(1)
        if found == "arc": return "intel arc graphics"
        if found == "iris": return "intel iris xe"
        if found == "uhd": return "intel uhd graphics"

    # 4. Apple
    apple_match = pt.apple_gpu_pattern.search(text)
    if apple_match:
        return apple_match.group(1)                  # Örn: m2, m4
    utils.logging_file("gpu_warnings")
    return None 