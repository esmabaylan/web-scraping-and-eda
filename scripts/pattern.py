import pandas as pd
import re

nvidia_gpu_pattern = re.compile(
    r"""
    (rtx|gtx|mx)                # Group 1: Prefix (RTX, GTX, MX)
    \s*
    (pro\s*|a)?                 # Group 2: Workstation serileri (PRO veya A)
    (\d{3,4}a?)                 # Group 3: Model Numarası (570a gibi istisnalar dahil)
    \s*
    (ti|ada)?                   # Group 4: Suffix (Ti, Ada)
    """,
    re.IGNORECASE | re.VERBOSE
)

amd_gpu_pattern = re.compile(
    r"""
    (radeon)                    # Radeon ibaresi
    \s*
    (\d{3}m?)?                  # 780m gibi spesifik numaralar (opsiyonel)
    """,
    re.IGNORECASE | re.VERBOSE
)

intel_gpu_pattern = re.compile(
    r"(arc|iris|uhd)",          # Intel için kilit kelimeler
    re.IGNORECASE | re.VERBOSE
)

apple_gpu_pattern = re.compile(
    r"\b(m[1-4])\b",            # Sadece M1, M2, M3, M4 
    re.IGNORECASE | re.VERBOSE
)
