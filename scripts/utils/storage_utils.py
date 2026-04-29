import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import scripts.pattern.storage_pattern as pt
import regex as re
import scripts.utils.utils as utils
import pandas as pd
import numpy as np

import pandas as pd
import scripts.pattern.storage_pattern as pt # Pattern dosyanı import et (yolunu kendine göre uyarla)

def handle_storage(text):
    if pd.isna(text):
        return None
        
    text = utils.normalize_text(text)
    
    # Standart kabul edilen depolama kapasiteleri (Örn: Casper'ın 480GB'ı veya özel 6TB kurulumlar dahil)
    valid_gb = {120, 128, 240, 250, 256, 480, 500, 512, 1000, 1024, 2000, 2048}
    valid_tb = {1, 2, 3, 4, 6, 8}
    ram_gb = {4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96, 128} # RAM ile çakışmayı önlemek için
    
    # 1. ADIM: "SSD", "HDD", "NVME" kelimeleriyle bitişik olanları bul
    match = pt.explicit_storage_pattern.search(text)
    if match:
        if match.group(1):
            val, unit = match.group(1), (match.group(2) or "GB").upper()
        elif match.group(3):
            val, unit = match.group(3), match.group(4).upper()
        elif match.group(5):
            val, unit = match.group(5), "GB" # Sadece "512ssd" yazılmışsa GB kabul et
            
        unit = "TB" if unit.startswith("T") else "GB"
        val_int = int(val)
        
        # Değerler mantıklı bir depolama boyutu mu?
        if unit == "GB" and val_int in valid_gb:
            return f"{val_int} {unit}"
        elif unit == "TB" and val_int in valid_tb:
            return f"{val_int} {unit}"
            
    # 2. ADIM: Sadece "1TB" veya "512GB" yazıp bırakanları bul (SSD/HDD yazmamış)
    for match in pt.general_storage_pattern.finditer(text):
        val = int(match.group(1))
        unit_raw = match.group(2).upper()
        unit = "TB" if unit_raw.startswith("T") else "GB"
        
        if unit == "TB" and val in valid_tb:
            return f"{val} {unit}" # 1TB, 2TB laptopta RAM olamayacağına göre kesin depolamadır.
            
        elif unit == "GB" and val in valid_gb:
            # Kritik Kontrol: Acaba bu "128GB" depolama mı yoksa RAM mi?
            if val in ram_gb:
                start = max(0, match.start() - 15)
                end = min(len(text), match.end() + 15)
                context = text[start:end].lower()
                # Eğer çevresinde RAM/DDR geçiyorsa bu depolama değildir, pas geç!
                if "ram" in context or "ddr" in context or "sodimm" in context:
                    continue
            return f"{val} {unit}"

    return None