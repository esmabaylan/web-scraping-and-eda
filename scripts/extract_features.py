import re

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Türkçe karakter problemi (İ → I)
    text = text.replace("İ", "I").replace("ı", "i")
    # Türkçe karakter problemi (Ö → O)
    text = text.replace("Ö", "O").replace("ö", "o")
    # Türkçe karakter problemi (Ü → U)
    text = text.replace("Ü", "U").replace("ü", "u")
    # Türkçe karakter problemi (Ç → C)
    text = text.replace("Ç", "C").replace("ç", "c")
    # Türkçe karakter problemi (Ş → S)
    text = text.replace("Ş", "S").replace("ş", "s")
    # Türkçe karakter problemi (Ğ → G)
    text = text.replace("Ğ", "G").replace("ğ", "g")


    # Küçük harfe çevir
    text = text.lower()

    # Virgül ve tireleri boşluk yap
    text = re.sub(r"[,\-]", " ", text)

    # Gereksiz kelimeleri temizle
    text = re.sub(r"\b(işlemci|graphics|ram|ssd|windows)\b", " ", text)

    # Fazla boşlukları tek boşluk yap
    text = re.sub(r"\s+", " ", text).strip()

    return text

series_pattern=re.compile(
    r"""
    (TUF|ROG|VivoBook|ZenBook|ExpertBook|ProArt|StudioBook)
    """,
    re.IGNORECASE | re.VERBOSE
)

def extract_series(text):
    if not isinstance(text, str):
        return None
    text = normalize_text(text)

    match = series_pattern.search(text)
    if match:
        return match.group(0)
    return None


cpu_pattern = re.compile(
    r"""
    # ================= INTEL =================

    (
        (intel\s*)?
        (core\s*)?
        (ultra\s*)?
        i[3579]                    # i5, i7, i9
        \s*[-]?\s*
        (\d{4,5}[a-z]{0,2})?       # 13450HX, 14650HX (opsiyonel)
    )

    |
    (
    
        (intel\s*)?
        core\s*
        [57]                       # Core 5 / Core 7
        \s*
        (\d{3,5}[a-z]{0,2})?
    )

    |
    # ================= AMD =================
(
        (amd\s*)?       # "amd" opsiyonel
        (ryzen|r)       # DİKKAT: Parantez içine aldık. "ryzen" VEYA "r" olabilir.
        \s* # Arada boşluk olabilir
        [3579]          # 3, 5, 7, 9 serisi
        \s*
        (\d{3,4}[a-z]{0,2})? # Model numarası (5800H gibi)
    )

    |
    # ================= APPLE =================
    (apple\s*)?(m[123](\s*(pro|max|ultra))?)

    """,
    re.IGNORECASE | re.VERBOSE
)


def extract_cpu(text):
    if not isinstance(text, str):
        return None
    text = normalize_text(text)

    text = text.lower()
    match = cpu_pattern.search(text)

    if not match:
        return None

    raw = match.group(0)

    raw = raw.replace("-", " ").replace(",", " ")
    raw = re.sub(r"\s+", " ", raw).strip()

    raw = re.sub(r"\s+", " ", raw).strip()

    raw = re.sub(r"(işlemci|processor|cpu)", "", raw).strip()
    raw = re.sub(r"\br\s*([3579])", r"ryzen \1", raw)

    if re.search(r"\bi[3579]\b", raw):
        if "intel" not in raw:
            raw = "intel core " + raw
    if re.search(r"\bR[3579]?\b", raw):
        if "amd" not in raw:
            raw = "amd " + raw

    raw = raw.title()
    raw = raw.replace("I5", "i5").replace("I7", "i7").replace("I9", "i9")
    raw = raw.replace("Core I", "Core i")

    return raw
