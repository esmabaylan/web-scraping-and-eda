import pandas as pd
import numpy as np
import joblib

# 1. Modeli Yükle
model = joblib.load("/work/model/best_laptop_model.joblib")

laptop = pd.DataFrame([{
    "ram_gb": 32.0,
    "storage_gb": 1024.0,
    "cpu_priority": 4.0,
    "gpu_priority": 4.0,
    "ram_priority": 4.0,
    "storage_priority": 3.0,
    "os_priority": 1.0,
    
    "cpu_ryzen_series": 7.0,      # Ryzen 7 (AMD olduğu için burası dolu)
    "intel_core_series": np.nan,  # AMD olduğu için Intel nan (boş) bırakılır
    "cpu_gen_num": 7.0,           # Örneğin Ryzen 7000 serisi için 7
    "gpu_has": 0,                 # Harici GPU var
    
    "extract_cpu_brand": "amd",   # "intel"  "amd"
    "os": "windows",
    "brand": "lenovo",
    "usage_purpose": "office"     # gaming, ofis, vb
}])

# 3. Tahmin Al
tahmini_fiyat = model.predict(laptop)

print(f"{laptop['extract_cpu_brand'].iloc[0].upper()} sistemli ve {laptop['usage_purpose'].iloc[0]} amaçlı bu laptop için tahmini fiyat: {tahmini_fiyat[0]:,.2f} TL")