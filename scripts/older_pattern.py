import regex as re


intel_cpu_pattern = re.compile(
    r"\b"+r"""
    \b
    (
        (intel\s*)?
        (core\s*)?
        (ultra\s*)?
        i[3579]                    # i5, i7, i9
        \s*[-]?\s*
        (\d{4,5}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC]){0,2})?       # 13450HX, 14650HX (opsiyonel)
    )
    \b

    |
    
    \b
    (
    
        (intel\s*)?
        core\s*
        [57]                       # Core 5 / Core 7
        \s*[-]?\s*
        (\d{3,5}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC]){0,2})?
    )
    \b
    
    |
    
    \b
    (ultra\s*)
    \s*?
    [3579]                       # 5, 7, 9 serisi (ultra ile birlikte)
    \s*[-]?\s*
    (\d{3,5}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC]){0,2})?
    \b
    
    |
    
    \b
    [3579]
    \s*[-]\s*?
    (\d{3,5}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC]){0,2})       # Sadece serisi ve model numarası (i7 1165G7 gibi)
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
            \d{3,4}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC])?         # Sadece sayı olan eski modeller
        )?
    )
    \b

    |
    
    (intel®\s*)                 # "Intel®" yazabilir yazmayabilir
    (core™\s*)                   # "Core" yazabilir yazmayabilir
    [3579]                      # 3, 5, 7, 9 serisi
    \s*[-]?\s*
    (\d{3,5}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC]){0,2})?       
    
    
    |

    \b
    (intel\s*)?                 # "Intel" yazabilir yazmayabilir
    (core\s*)?                   # "Core" yazabilir yazmayabilir
    (u[3579]\s*)              # "u3", "u5", "u7" opsiyonel
    \s*?
    [-]?
    \s*?
    (\d{3,5}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC]){0,2})?        # Model numarası (1165G7 gibi)
    \b

    |

    \b[3579]\s+\d{3,4}[a-zA-Z]{1,2}\b 
    
    |

    \b(\d{3,5}(HX|HS|HK|KF|KS|X3D|XT|GE|G[1-7]|[UHPKFTXGC]){0,2})\b

    
    """,
    re.VERBOSE,re.IGNORECASE
)

amd_cpu_pattern=re.compile(
    r"\b"+r"""
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
    
    # 4552
    (
        (R[-][3579])                # R-5, R-7, R-9 serisi
        (\s*[-]?\s*\d{3,5}[a-z]{0,2})?  # Model numarası (370 gibi)
    )
    |    
    #Um5606Wa-Rk295W AMD Ryzen AI 9 Hx370 32Gb RAM 1TB SSD AMD Radeon Graphics 16" 3K Oled Win11 Bey    
    (amd\s*)?                   # "amd" opsiyonel
    ((ryzen|r|ryzen™|r™)\s*)                 # "ryzen" opsiyonel
    (AI\s*)                   # "AI" opsiyonel
    (5|7|9)                      # 5, 7, 9 serisi
    (?:\s*hx)?                   # "hx" opsiyonel (örneğin Ryzen 9 Hx370 gibi)
    \s*[-]?\s*
    (\d{3,5}[a-z]{0,2})?        # Model numarası (370 gibi)
    
    |
    (
    (amd\s*)?                   # "amd" opsiyonel
    (ryzen|r)                 # "ryzen" veya "r" (yakalamayan grup)
    ™?
    \s*?
    (ai\s*)                   # "AI" opsiyonel
    (z2\s*)                      # 5, 7, 9 serisi
    (\d{3,5}[a-z]{0,2})?        # Model numarası (370 gibi)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

apple_cpu_pattern = re.compile(
    r"\b"+r"""
    # ================= APPLE =================
    (apple\s*)?(m[123](\s*(pro|max|ultra))?)
    """,
    re.IGNORECASE | re.VERBOSE
)

snapdragon_cpu_pattern=re.compile(
    r"\b"+r"""
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




asus_series_pattern = re.compile(
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


ram_pattern = re.compile(
r"""
    (
        # SENARYO 1: Önünde DDR/LPDDR olanlar (GB olsa da olmasa da yakalar)S
        (
        (lp)?
        ddr[345]x?\s+
        )
        (\d{1,3})(\s*GB)?
        |
        # SENARYO 2: Önünde DDR yoksa, GB birimi ZORUNLU (Hatalı sayıları eler)
        (
        (lp)?
        ddr[345]x?
        \s*)?
        (\d{1,3})(\s*(GB))
        

    )
    """,
    re.IGNORECASE | re.VERBOSE
)

stroge_pattern = re.compile(
    r"""

    \b                          
    (\d+)                       
    \s*                         
    (TB|GB|T|G)                    
    \s*                         
    (SSD|M\.?2|NVMe|PCIe)?      
    \b

    |

    \b                          
    (\d+)                       
    \s*                         
    (TB|GB|T|G)?                    
    \s*                         
    (SSD|M\.?2|NVMe|PCIe)      
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
