import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import scripts.pattern.cpu_pattern as pt
import regex as re
import logging as log
import scripts.utils.utils as utils

import pandas as pd

import numpy as np
def get_cpu_patterns():
    return {
        "intel": pt.intel_cpu_pattern,
        "amd": pt.amd_cpu_pattern,
        "snapdragon": pt.snapdragon_cpu_pattern,
        "apple": pt.apple_cpu_pattern
    }

def handle_cpu(text):
    if pd.isna(text):
        return None
    text = utils.normalize_text(text)

    matches = list(pt.intel_cpu_pattern.finditer(text))
    if matches:
        return max(matches, key=lambda m: len(m.group(0))).group(0)

    matches = list(pt.amd_cpu_pattern.finditer(text))
    if matches:
        return max(matches, key=lambda m: len(m.group(0))).group(0)

    matches = list(pt.snapdragon_cpu_pattern.finditer(text))
    if matches:
        return max(matches, key=lambda m: len(m.group(0))).group(0)

    matches = list(pt.apple_cpu_pattern.finditer(text))
    if matches:
        return max(matches, key=lambda m: len(m.group(0))).group(0)

    return None
