import regex as re

import re

intel_cpu_pattern = re.compile(
    r"""
    \b
    (
        # Intel Core i7-13700H, i9-14900HX, i5-1035G7
        (?:intel\s*)?
        (?:core\s*)?
        i[3579]
        \s*[-]?\s*
        \d{4,5}(?:HX|HK|HQ|KS|KF|TE|XE|QM|H|U|P|Y|K|F|T|X|M|V|G[1-7])?
    )
    \b
    |
    \b
    (
        # Core 7 240H / Core 5-120U
        (?:intel\s*)?
        core\s*
        [3579]
        \s*[-]?\s*
        \d{3,5}(?:HX|HK|HQ|H|U|P|V)?
    )
    \b
    |
    \b
    (
        # Ultra 7 255H / Ultra7-255H / Ultra 7 258V
        ultra\s*
        [3579]
        \s*[-]?\s*
        \d{3,5}(?:HX|HK|H|U|V)?
    )
    \b
    |
    \b
    (
        # U7-255H / U9-275HX
        u[3579]
        \s*[-]?\s*
        \d{3,5}(?:HX|H|U|V)?
    )
    \b
    |
    \b
    (
        # i7 13620H (Sadece 1 veya 2 harf bekleyen özel blok)
        i[3579]
        \s+
        \d{3,5}(?:HX|HK|HQ|KS|KF|TE|XE|QM|H|U|P|Y|K|F|T|X|M|V|G[1-7])
    )
    \b
    """, 
    re.IGNORECASE | re.VERBOSE)


amd_cpu_pattern=re.compile(        
    r"""
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
        )?
        (pro|)                          # Model numarası opsiyonel
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
    re.VERBOSE | re.IGNORECASE
    )

snapdragon_cpu_pattern=re.compile(    
    r"""
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
    re.VERBOSE | re.IGNORECASE)

apple_cpu_pattern=re.compile(    
    r"""
    # ================= APPLE =================
    (apple\s*)?(m[123](\s*(pro|max|ultra))?)
    
    """,
    re.VERBOSE | re.IGNORECASE
    )