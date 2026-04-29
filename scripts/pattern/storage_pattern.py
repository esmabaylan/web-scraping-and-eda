import regex as re

explicit_storage_pattern = re.compile(
    r"\b(\d{1,4})\s*[-]?\s*(TB|T|GB|G)?\s*[-]?\s*(?:SSD|HDD|NVME|M\.2|PCIE|SSHD)\b|"
    r"\b(?:SSD|HDD|NVME|M\.2|PCIE|SSHD)\s*(\d{1,4})\s*[-]?\s*(TB|T|GB|G)\b|"
    r"\b(\d{1,4})\s*(?:SSD|HDD|NVME)\b",  # Örn: "512ssd" (GB yazmayı unutanlar için)
    re.IGNORECASE | re.VERBOSE
)

general_storage_pattern = re.compile(
    r"\b(\d{1,4})\s*[-]?\s*(TB|T|GB|G)\b", 
    re.IGNORECASE | re.VERBOSE
)