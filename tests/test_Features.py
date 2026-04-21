# test_extract_features.py
import pytest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '..'))


sys.path.append(project_root)

from scripts import extract_features
import pandas as pd
import scripts.utils.utils as utils



def test_extract_gpu():
    csv_path = os.path.join(project_root, "data", "evaluate_data", "gpu_extracted.csv")
    golden_df = pd.read_csv(csv_path)
    real_tag=golden_df["manual_gpu"]
    extract_tag= golden_df["name"].apply(lambda x: extract_features.extract_gpu(x))


    counter = 0
    for name,real, extract in zip(golden_df["name"],real_tag, extract_tag):
        if utils.normalize_text(real) != utils.normalize_text(extract):
            print(f"Name: {name}")
            print(f"Mismatch: Expected: {real}, Got: {extract}",end="\n------------\n")
            counter += 1

    assert counter == 0, f"Found {counter} mismatches"


def test_extract_cpu():
    pass


