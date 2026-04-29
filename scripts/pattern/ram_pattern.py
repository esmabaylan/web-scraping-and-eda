import regex as re
import pandas as pd

# 1. KESİN RAM İFADELERİ (Örn: "16GB RAM", "32GB DDR5", "SODIMM 8GB", "16 GB5")
explicit_pattern = re.compile(
    r"\b(\d{1,3})\s*[-]?\s*(?:GB|G)5?\s*(?:RAM|DDR[2-5]|LPDDR[2-5]X?|SODIMM|BELLEK)\b|"
    r"\b(?:RAM|DDR[2-5]|LPDDR[2-5]X?|SODIMM|BELLEK)\s*(\d{1,3})\s*[-]?\s*(?:GB|G)5?\b",
    re.IGNORECASE|re.VERBOSE
)

        
# 2. ESNEK ARAMA (Depolama Disklerini Hariç Tut)
# Etrafında SSD, HDD, NVME geçmeyen düz "16GB" gibi sayıları bulur.
general_pattern = re.compile(
    r"\b(\d{1,3})\s*[-]?\s*(?:GB|G)5?\b(?!\s*[-]?\s*(?:SSD|HDD|NVME|DISK|EMMC))", 
    re.IGNORECASE|re.VERBOSE
)
    
# 3. SON ÇARE (Hiçbir kurala uymayan "16 GB" gibi yalnız kalmış değerler)
all_ram_pattern = re.compile(r"\b(\d{1,3})\s*[-]?\s*(?:GB|G)5?\b", re.IGNORECASE|re.VERBOSE)
