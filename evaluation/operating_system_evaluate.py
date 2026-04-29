import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))


import pandas as pd

from scripts.utils.os_utils import handle_os

df=pd.read_csv("data/evaluate_data/sample_data/os_sample.csv")


extract_tag= df["name"].apply(lambda x: handle_os(x))

real_tag=pd.read_csv("data/evaluate_data/golden_data/os_labeled.csv")


counter = 0
with open("data/evaluate_data/missmatchData/os_mismatches.txt", "w") as f:
    for name,real, extract in zip(df["name"],real_tag["manual_os"], extract_tag):
        real = real.lower() if isinstance(real, str) else real
        extract = extract.lower() if isinstance(extract, str) else extract
        if real != extract and not (pd.isna(real) and pd.isna(extract)):
            f.write(f"Name: {name}\n")
            f.write(f"Mismatch: Expected: {real}, Got: {extract}\n")
            f.write("------------\n")
            counter += 1

print(f"Total mismatches: {counter}")
print(real_tag.head(2))
print(extract_tag.head(2))

df.drop(columns=["manual_os"], inplace=True, errors='ignore')
df["extracted_os"] = extract_tag
df.to_csv("data/evaluate_data/extracted_data/os_extracted.csv", index=False)