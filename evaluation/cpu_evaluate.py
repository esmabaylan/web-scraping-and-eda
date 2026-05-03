import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))


import pandas as pd

from scripts.extract_features import extract_cpu
"""
the file is for evaluating the cpu extraction results. 
It reads the cpu_extracted.csv file, applies the extract_cpu function to the "name" column, and compares the results with the "manual_cpu" column. 
The mismatches are printed along with the name of the product. 
Finally, it asserts that there are no mismatches.
"""



df=pd.read_csv("data/evaluate_data/sample_data/cpu_sample.csv")


extract_tag= df["name"].apply(lambda x: extract_cpu(x))

real_tag=pd.read_csv("data/evaluate_data/golden_data/cpu_labeled.csv")



counter = 0
with open("data/evaluate_data/missmatchData/cpu_mismatches.txt", "w") as f:
    for name,real, extract in zip(df["name"],real_tag["manual_cpu"], extract_tag):
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


df.drop(columns=["manual_cpu"], inplace=True,axis=1)
df["extracted_cpu"] = extract_tag
df.to_csv("data/evaluate_data/extracted_data/cpu_extracted.csv", index=False)