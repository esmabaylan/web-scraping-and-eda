import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from scripts.extract_features import extract_gpu


df=pd.read_csv("data/evaluate_data/gpu_extracted.csv")

df.drop(columns="manual_gpu", inplace=True,axis=1)

real_tag=df["golden_gpu"]

extract_tag= df["name"].apply(lambda x: extract_gpu(x))

print(real_tag.head(2))
print(extract_tag.head(2))
