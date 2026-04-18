import pandas as pd
import re
import io

def standardize_gpu(text):
    if pd.isna(text):
        return "None"
    
    # Metni tamamen küçük harfe çevirip işlem yapıyoruz
    text = str(text).lower()
    
    # 1. RTX ve GTX Serisi (Örn: rtx 4060, rtx 5070ti, rtx pro 1000, rtx 500 ada)
    # Ürün kodlarındaki (örn: 21SR006RTXH23) sahte eşleşmeleri önlemek için arkasından rakam arıyoruz.
    rtx_match = re.search(r'(rtx|gtx)\s*(pro\s*)?(\d{3,4})\s*(ti|ada)?', text)
    if rtx_match:
        prefix = rtx_match.group(1) # rtx veya gtx
        pro = rtx_match.group(2) or "" # pro kelimesi varsa
        number = rtx_match.group(3) # 4060, 5070 vb.
        suffix = rtx_match.group(4) or "" # ti veya ada
        
        # Parçaları birleştir ve fazladan oluşan boşlukları temizle
        result = f"{prefix} {pro.strip()} {number}{suffix}".replace("  ", " ").strip()
        return result
        
    # 2. NVIDIA Workstation (RTX A serisi - Örn: rtx a500)
    rtxa_match = re.search(r'rtx\s*a(\d{3,4})', text)
    if rtxa_match:
        return f"rtx a{rtxa_match.group(1)}"
        
    # 3. NVIDIA MX Serisi (Örn: mx550, mx570a)
    mx_match = re.search(r'mx\s*(\d{3}a?)', text)
    if mx_match:
        return f"mx{mx_match.group(1)}"
        
    # 4. Intel Grafikleri (Arc, Iris, UHD)
    if 'arc' in text:
        return 'intel arc graphics'
    if 'iris' in text:
        return 'intel iris xe'
    if 'uhd' in text:
        return 'intel uhd graphics'
        
    # 5. AMD Radeon Serisi (Örn: radeon 780m)
    radeon_match = re.search(r'radeon\s*(\d{3}m?)', text)
    if radeon_match:
        return f"radeon {radeon_match.group(1)}"
    if 'radeon' in text:
        return 'amd radeon'
        
    # 6. Apple Silicon (M Serisi Çipler - Örn: m2, m4)
    # \b sınırlandırıcıları ile sadece kelime olarak "m2" veya "m4" geçiyorsa alır
    apple_match = re.search(r'\b(m[1-4])\b', text)
    if apple_match:
        return apple_match.group(1)
        
    # Hiçbir kalıba uymuyorsa harici/bilinen bir GPU yoktur
    return "None"

# --- KULLANIM ---

# 1. Aşama: Veri setini yükle (Aşağıdaki dosya adını kendi .csv dosyanla değiştir)
# df = pd.read_csv('ham_veriseti.csv')

# ÖRNEK: Senin attığın verinin bir kısmını dataframe olarak test edelim
df = pd.read_csv("data/evaluate_data/gpu_sample.csv")

# 2. Aşama: Script'i uygula ve yeni altın standart sütununu oluştur
df['golden_gpu'] = df['name'].apply(standardize_gpu)

# Karşılaştırmak için ekrana yazdır (Notebook ortamındaysan display(df) kullanabilirsin)
print(df[['name', 'manual_gpu', 'golden_gpu']])

df.drop(columns="manual_gpu", inplace=True, axis=1)
df.to_csv('data/evaluate_data/gpu_extracted.csv', index=False)
