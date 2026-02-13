import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests import test_cases
from scripts import extract_features
import pandas as pd

def test_extract_series():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted series: {extract_features.extract_series(e)}")
        print()


def test_cpu_extraction():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted CPU: {extract_features.extract_cpu(e)}")
        print()


def test_gpu_extraction():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted GPU: {extract_features.extract_gpu(e)}")
        print()

def test_extract_ram():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted RAM: {extract_features.extract_ram(e)}")
        print() 

def test_extract_os():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted OS: {extract_features.extract_os(e)}")
        print()

def test_extract_storage():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted Storage: {extract_features.extract_storage(e)}")
        print()

def test_all_features():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        features = extract_features.get_features(e)
        print(f"Extracted features: {features}")
        print()


def test_remove_features():
    for i, e in enumerate(test_cases.test_asus_cases):
        print(f"Test case {i}: {e}")
        extract_features.remove_features(e)
        print()
        break

if __name__ == "__main__":
    # test_cpu_extraction()
    # test_gpu_extraction()
    # test_extract_ram()
    # test_extract_os()
    test_extract_storage()
    # test_all_features()
    # test_remove_features()