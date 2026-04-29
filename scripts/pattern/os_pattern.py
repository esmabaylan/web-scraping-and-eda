import regex as re

# Apple
macos_pattern = re.compile(r"\b(macbook|macos|mac\s*os)\b", re.IGNORECASE| re.VERBOSE)

# FreeDOS
freedos_pattern = re.compile(r"\b(freedos|fdos|dos|no\s*os|freed|fd)\b", re.IGNORECASE| re.VERBOSE)

# Windows 11
win11_pattern = re.compile(r"(?:win\s*11|w11|windows\s*11|11\s*home|11\s*pro|w1$)\s*(home|pro|p|h)?", re.IGNORECASE| re.VERBOSE)

# Windows 10
win10_pattern = re.compile(r"(?:win\s*10|w10|windows\s*10|10\s*home|10\s*pro)\s*(home|pro|p|h)?", re.IGNORECASE| re.VERBOSE)

# Linux
linux_pattern = re.compile(r"\b(ubuntu|linux)\b", re.IGNORECASE| re.VERBOSE)

# Android / Tablet
android_pattern = re.compile(r"\b(matepad|android|harmonyos)\b", re.IGNORECASE| re.VERBOSE)

# Genel Windows
win_generic_pattern = re.compile(r"\b(windows|win)\b", re.IGNORECASE| re.VERBOSE)