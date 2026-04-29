import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import scripts.pattern.ram_pattern as pt
import regex as re
import scripts.utils.utils as utils
import pandas as pd
import numpy as np


def get_ram_patterns():
    return {
        "explicit": pt.explicit_pattern,
        "general": pt.general_pattern,
        "all_matches": pt.all_ram_pattern
    }


def handle_ram(text):
    if pd.isna(text):
        return None
    text = utils.normalize_text(text)
    
    valid_ram_sizes = {4, 6, 8, 10, 12, 16, 18, 20, 24, 32, 36, 40, 48, 64, 72, 80, 96, 128}
    
    for match in pt.explicit_pattern.finditer(text):
        val_str = match.group(1) if match.group(1) else match.group(2)
        val = int(val_str)
        if val in valid_ram_sizes:
            return f"{val} GB"
        
    matches = list(pt.general_pattern.finditer(text))
    fallback_match = None
    
    for m in matches:
        val = int(m.group(1))
        if val not in valid_ram_sizes:
            continue
            
        # VRAM (Ekran Kartı Belleği) TUZAĞINDAN KAÇINMA:
        # Bulduğumuz GB değerinin sağında ve solunda RTX, GTX gibi terimler var mı bakıyoruz.
        # Amacımız "RTX4060 8GB" kısmındaki 8GB'ı sistem RAM'i sanmamak.
        start = max(0, m.start() - 20)
        end = min(len(text), m.end() + 20)
        context = text[start:end].lower()
        
        gpu_terms = ["rtx", "gtx", "rx", "radeon", "arc", "vga", "vram", "gddr"]
        is_vram = any(term in context for term in gpu_terms)
        
        if not is_vram:
            return f"{val} GB"
        else:
            # Belki cümlede başka RAM yazmıyordur, bu 8GB hem sistem hem ekran kartı olabilir diye yedekte tutuyoruz.
            if not fallback_match:
                fallback_match = f"{val} GB"
                
    if fallback_match:
        return fallback_match
    
    for m in pt.all_matches:
        val = int(m.group(1))
        if val in valid_ram_sizes:
            return f"{val} GB"
             
    return None