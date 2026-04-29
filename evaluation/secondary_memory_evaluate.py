import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from scripts.extract_features import extract_storage


df=pd.read_csv("data/evaluate_data/sample_data/storage_sample.csv")


extract_tag= df["name"].apply(lambda x: extract_storage(x))

real_tag=pd.read_csv("data/evaluate_data/golden_data/storage_labeled.csv")

counter = 0
with open("data/evaluate_data/missmatchData/storage_mismatches.txt", "w") as f:
    for name,real, extract in zip(df["name"],real_tag["manual_storage"], extract_tag):
        if real != extract and not (pd.isna(real) and pd.isna(extract)):
            f.write(f"Name: {name}\n")
            f.write(f"Mismatch: Expected: {real}, Got: {extract}\n")

            print(f"{name}\n Mismatch: Expected: {real}, Got: {extract}\n")
            f.write("------------\n")
            counter += 1

print(f"Total mismatches: {counter}")

print(real_tag.head(2))
print(extract_tag.head(2))

df.drop(columns=["manual_storage"], inplace=True,axis=1)
df["extracted_storage"] = extract_tag
df.to_csv("data/evaluate_data/extracted_data/storage_extracted.csv", index=False)


