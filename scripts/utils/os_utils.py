import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import regex as re
import scripts.utils.utils as utils
import pandas as pd
import numpy as np
import scripts.pattern.os_pattern as os_pt
import pandas as pd
import scripts.pattern.os_pattern as os_pt
import scripts.utils.utils as utils

def handle_os(text):
    if pd.isna(text):
        return None
        
    # Metni tamamen küçük harfe çevirip temizliyoruz ki büyük/küçük harf çökmesi yaşanmasın
    text = utils.normalize_text(str(text))
    if not text:
        return None
    
    # 1. MacOS
    if os_pt.macos_pattern.search(text):
        return "macOS"
        
    # 2. FreeDOS / DOS
    if os_pt.freedos_pattern.search(text):
        return "FreeDOS"
        
    # 3. Windows 11 (Home / Pro / Genel)
    w11_match = os_pt.win11_pattern.search(text)
    if w11_match:
        matched_str = w11_match.group(0)
        suffix = w11_match.group(1) 
        
        if 'pro' in matched_str or suffix == 'p':
            return "Windows 11 Pro"
        elif 'home' in matched_str or suffix == 'h':
            return "Windows 11 Home"
        return "Windows 11"
        
    # 4. Windows 10 (Home / Pro / Genel)
    w10_match = os_pt.win10_pattern.search(text)
    if w10_match:
        matched_str = w10_match.group(0)
        suffix = w10_match.group(1)
        
        if 'pro' in matched_str or suffix == 'p':
            return "Windows 10 Pro"
        elif 'home' in matched_str or suffix == 'h':
            return "Windows 10 Home"
        return "Windows 10"
        
    # 5. Linux / Ubuntu
    if os_pt.linux_pattern.search(text):
        return "Linux"
        
    # 6. Android / HarmonyOS (Tabletler için)
    if os_pt.android_pattern.search(text):
        return "Android / HarmonyOS"
        
    # 7. Son Çare (Düz Windows)
    if os_pt.win_generic_pattern.search(text):
        return "Windows"

    return None