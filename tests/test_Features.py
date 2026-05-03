import pytest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from scripts import extract_features
import pandas as pd
import scripts.utils.utils as utils

def run_feature_test(csv_path, manual_col, extract_fn):
    df = pd.read_csv(csv_path)
    counter = 0
    for name, real, extracted in zip(df["name"], df[manual_col], df["name"].apply(extract_fn)):
        if utils.normalize_text(real) != utils.normalize_text(extracted):
            print(f"Name: {name}")
            print(f"Mismatch: Expected: {real}, Got: {extracted}\n------------")
            counter += 1
    assert counter == 0, f"Found {counter} mismatches"


def test_extract_gpu():
    csv_path = os.path.join(project_root, "data", "evaluate_data","golden_data", "gpu_labeled.csv")

    run_feature_test(csv_path, "manual_gpu", extract_features.extract_gpu)

def test_extract_cpu():
    csv_path = os.path.join(project_root, "data", "evaluate_data","golden_data", "cpu_labeled.csv")
    run_feature_test(csv_path, "manual_cpu", extract_features.extract_cpu)
   

def test_extract_ram():
    csv_path = os.path.join(project_root, "data", "evaluate_data","golden_data", "ram_labeled.csv")
    run_feature_test(csv_path, "manual_ram", extract_features.extract_ram)


def test_extract_os():
    csv_path = os.path.join(project_root, "data", "evaluate_data","golden_data", "os_labeled.csv")
    run_feature_test(csv_path, "manual_os", extract_features.extract_os)

def test_extracted_storage():
    csv_path = os.path.join(project_root, "data", "evaluate_data","golden_data", "storage_labeled.csv")
    run_feature_test(csv_path, "manual_storage", extract_features.extract_storage)