import re

cpu_pattern = re.compile(
    r"\b"+r"""
    # ================= INTEL =================
    \b
    (
        (intel\s*)?
        (core\s*)?
        (ultra\s*)?
        i[3579]                    # i5, i7, i9
        \s*[-]?\s*
        (\d{4,5}[a-z]{0,2})?       # 13450HX, 14650HX (opsiyonel)
    )
    \b
    |
    \b
    (
    
        (intel\s*)?
        core\s*
        [57]                       # Core 5 / Core 7
        \s*[-]?\s*
        (\d{3,5}[a-z]{0,2})?
    )
    \b
    |
    \b
    (ultra\s*)
    \s*?
    [3579]                       # 5, 7, 9 serisi (ultra ile birlikte)
    \s*[-]?\s*
    (\d{3,5}[a-z]{0,2})?
    \b
    |
    \b
    [3579]
    \s*[-]\s*?
    (\d{3,5}[a-z]{0,2})       # Sadece serisi ve model numarası (i7 1165G7 gibi)
    \b
    |
    \b
    (
        (intel\s*)?
        (celeron|pentium)         # Celeron veya Pentium kelimesini zorunlu kıldık
        \s*
        (
            [njg]\d{3,4}          # N4020, J4125, G5900 gibi modeller
            |                     # VEYA
            \d{3,4}[a-z]?         # Sadece sayı olan eski modeller
        )?
    )
    \b
    |
    # ================= AMD =================
(
        (amd\s*)?                   # "amd" opsiyonel
        (?:ryzen|r)                 # "ryzen" veya "r" (yakalamayan grup)
        \s*™?
        \s*
        [3579]                      # 3, 5, 7, 9 serisi
        (?:                         # Model numarası için grup
            \s+                     # Arada mutlaka boşluk olmalı
            \d{4}                   # 7520 gibi 4 haneli sayı
            [a-z]{0,2}              # u, h, hs gibi ekler
        )?                          # Model numarası opsiyonel
    )

    |
    # ================= APPLE =================
    (apple\s*)?(m[123](\s*(pro|max|ultra))?)
    |
    # ================= Snapdragon =================
    (
        (qualcomm\s*)?              # "Qualcomm" yazabilir yazmayabilir
        snapdragon\s* # "Snapdragon" ZORUNLU
        (
            x\s*(elite|plus|[0-9])? # X Elite, X Plus veya X1
            |
            [87]c(\s*gen\s*\d)?     # Eski nesil: 7c Gen 2, 8cx
        )?
        (\s*[\w-]+)?                # Model Kodu Devamı (X1E-78-100 gibi)
    )

    """,
    re.IGNORECASE | re.VERBOSE
)

series_pattern = re.compile(
    r"""
    (TUF\s*)
    |
    (ROG\s*)
    |
    (VIVOBOOK\s*)
    |
    (ZENBOOK\s*)
    |
    (EXPERTBOOK\s*)
    |
    (PROART\s*)
    |
    (STUDIOBOOK\s*)
    |
    (X\d+
    [a-z]{0,3}
    )
    
    """,
    re.IGNORECASE | re.VERBOSE
)

gpu_pattern = re.compile(
    r"""
    # ================= NVIDIA =================
    (
        (?:\d{1,2}\s*GB\s+)?           # Başta opsiyonel VRAM (8GB RTX...)
        (?:nvidia\s*)?
        (?:geforce\s*)?
        (rtx|gtx)                      # RTX veya GTX zorunlu
        \s*
        (\d{3,4}(?:\s*ti|super)?)      # Model No: 3050, 4060 Ti vb.
        (?:\s*[-/]?\s*\d{1,2}\s*GB)?   # Sonda opsiyonel VRAM (...4050 6GB)
    )
    |
    # ================= AMD =================
    (
        (?:amd\s*)?
        (?:radeon\s+)?
        (rx|vega)\s* # RX veya Vega zorunlu
        (\d{3,4}(?:\s*xt)?)            # 6600 XT, 7600 vb.
        (?:\s*[-/]?\s*\d{1,2}\s*GB)?
    )
    |
    # ================= INTEL (KRİTİK DÜZELTME) =================
    (
        (?:intel\s*)?
        (
            iris\s*xe|                 # Spesifik modeller
            arc\s*[a-z]?\d{3}|         # Arc A750 vb.
            uhd\s*graphics\s*\d{0,3}|  # UHD Graphics 620 vb.
            hd\s*graphics\s*\d{0,3}    # Sadece "hd" yetmez, "graphics" de olmalı
        )
    )
    |
    # ================= APPLE =================
    (
        (?:apple\s*)?
        (m[1234](?:\s*(?:pro|max|ultra))?)\s*gpu
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

ram_pattern = re.compile(
r"""
    #================== RAM =================
    (?:RAM\s*[:\-]?\s*)?           # "RAM" etiketi (opsiyonel)
    
    (?:
        # SENARYO 1: Önünde DDR/LPDDR olanlar (GB olsa da olmasa da yakalar)
        ((?:lp)?ddr[345]x?\s+)(\d{1,3})(?:\s*GB)?
        |
        # SENARYO 2: Önünde DDR yoksa, GB birimi ZORUNLU (Hatalı sayıları eler)
        ((?:lp)?ddr[345]x?\s*)?(\d{1,3})(?:\s*GB)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

stroge_pattern = re.compile(
    r"""
    \b                          
    (\d+)                       
    \s*                         
    (TB|GB)                    
    \s*                         
    (SSD|M\.?2|NVMe|PCIe)?      
    \b                          
    """,
    re.IGNORECASE | re.VERBOSE
)

os_pattern = re.compile(
    r"""

    #================== Operatinf System =================
   (?:windows|win|w)\s*(?:1[01]|[78])|freedos|free\s*dos|dos|fdos|linux|ubuntu
    """,
    re.IGNORECASE | re.VERBOSE
)

