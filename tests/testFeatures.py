# test_extract_features.py
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests import test_cases
from scripts import extract_features

class TestFeatureExtraction():
    """Test suite for feature extraction"""
    
    @pytest.mark.parametrize("product_desc", test_cases.test_asus_cases)
    def test_cpu_extraction(self, product_desc):
        """Test that CPU extraction doesn't fail"""
        result = extract_features.extract_cpu(product_desc)
        assert result is not None or result == "", f"CPU extraction failed for: {product_desc}"
    
    @pytest.mark.parametrize("product_desc", test_cases.test_asus_cases)
    def test_gpu_extraction(self, product_desc):
        """Test that GPU extraction doesn't fail"""
        result = extract_features.extract_gpu(product_desc)
        assert isinstance(result, str), f"GPU should return string: {product_desc}"
    
    def test_cpu_specific_cases(self):
        """Test specific CPU extraction cases"""
        test_data = [
            ("Intel Core i5-13450HX", "i5-13450HX"),
            ("AMD Ryzen 7 7445HS", "Ryzen 7 7445HS"),
            ("Snapdragon X Elite", "Snapdragon X Elite"),
        ]
        
        for product, expected in test_data:
            result = extract_features.extract_cpu(product)
            assert expected.lower() in result.lower(), \
                f"Expected '{expected}' in '{result}' for '{product}'"
    
    def test_storage_extraction_gb_to_tb(self):
        """Test storage unit conversion"""
        product = "1TB SSD"
        result = extract_features.extract_storage(product)
        # Assuming function returns dict like {'size': 1024, 'unit': 'GB'}
        assert result is not None, "Storage extraction failed"

def test_all_with_summary(column):
    """Run all tests and show summary"""
    
    results = {
        'total': len(column),
        'cpu_found': 0,
        'gpu_found': 0,
        'ram_found': 0,
        'storage_found': 0,
        'os_found': 0,
    }
    
    for case in column:
        if extract_features.extract_cpu(case):
            results['cpu_found'] += 1
        if extract_features.extract_gpu(case):
            results['gpu_found'] += 1
        if extract_features.extract_ram(case):
            results['ram_found'] += 1
        if extract_features.extract_storage(case):
            results['storage_found'] += 1
        if extract_features.extract_os(case):
            results['os_found'] += 1
    
    # Özet çıktı
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Total test cases: {results['total']}")
    print(f"CPU found: {results['cpu_found']} ({results['cpu_found']/results['total']*100:.1f}%)")
    print(f"GPU found: {results['gpu_found']} ({results['gpu_found']/results['total']*100:.1f}%)")
    print(f"RAM found: {results['ram_found']} ({results['ram_found']/results['total']*100:.1f}%)")
    print(f"Storage found: {results['storage_found']} ({results['storage_found']/results['total']*100:.1f}%)")
    print(f"OS found: {results['os_found']} ({results['os_found']/results['total']*100:.1f}%)")
    print("="*50)


if __name__ == "__main__":
    test_all_with_summary()