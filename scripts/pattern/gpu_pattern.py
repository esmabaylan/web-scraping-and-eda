import re

# GPU pattern
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
    |
    (radeon|rx)                 # Radeon veya RX kelimesi
    \s*
    (\d{3,4}m?s?|xt)?           # 780m, 7600s, 6500xt gibi numaralar
    """,
    re.IGNORECASE | re.VERBOSE
)

intel_gpu_pattern = re.compile(
    r"(arc|iris|uhd|xe\s*graphics|intel\s*graphics)",          # Intel için kilit kelimeler
    re.IGNORECASE | re.VERBOSE
)

apple_gpu_pattern = re.compile(
    r"\b(m[1-4])\b",            # Sadece M1, M2, M3, M4 
    re.IGNORECASE | re.VERBOSE
)

