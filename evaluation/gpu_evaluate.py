import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from scripts.extract_features import extract_gpu

"""
the file is for evaluating the gpu extraction results.
It reads the gpu_extracted.csv file, applies the extract_gpu function to the "name" column, and compares the results with the "manual_gpu" column.
"""
df=pd.read_csv("data/evaluate_data/sample_data/gpu_sample.csv")


extract_tag= df["name"].apply(lambda x: extract_gpu(x))

real_tag=pd.read_csv("data/evaluate_data/golden_data/gpu_labeled.csv")

counter = 0
with open("data/evaluate_data/missmatchData/gpu_mismatches.txt", "w") as f:
    for name,real, extract in zip(df["name"],real_tag["manual_gpu"], extract_tag):
        if real != extract and not (pd.isna(real) and pd.isna(extract)):
            f.write(f"Name: {name}\n")
            f.write(f"Mismatch: Expected: {real}, Got: {extract}\n")

            print(f"{name}\n Mismatch: Expected: {real}, Got: {extract}\n")
            f.write("------------\n")
            counter += 1

print(f"Total mismatches: {counter}")

print(real_tag.head(2))
print(extract_tag.head(2))

df.drop(columns=["manual_gpu"], inplace=True,axis=1)
df["extracted_gpu"] = extract_tag
df.to_csv("data/evaluate_data/extracted_data/gpu_extracted.csv", index=False)


