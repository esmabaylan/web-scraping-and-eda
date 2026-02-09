import pandas as pd
from extract_features import extract_cpu, extract_series

test_asus_cases = [
     'TUF F16 FX608JH Gaming Intel Core i5-13450HX 16GB 512GB SSD RTX5050 16" FHD WUXGA 165Hz IPS Freedos',
     'Vivobook 15 X1504VA Intel Core 5 120U 16GB 512GB SSD 15.6" W11 + OFFİCE',
     'TUF F16 i7 14650HX 24GB 512GB SSD RTX5050/8GB 115W 165Hz 16'' WUXGA FDOS Gaming Laptop FX608JHR',
     'Vivobook 15 Intel Core 5 120U 16GB 512GB SSD W11 PRO 15.6" FHD + Mouse',
     'Fhd, İntel Core İ5 İşlemci, İntel GRAPHICS,16GB Ram,512GB Ssd, Windows 11-X1504VA',
     'TUF Gaming A16 FA607NUG-RL212 R7 7445HS 16GB 512GB SSD RTX4050-6GB 140W Dos 16" WUXGA 144Hz Notebook',
     'Vivobook 16 V3607VH-RP075 Intel Core 5-210H 16GB RAM 512GB SSD 8GB RTX5050 16" WUXGA 144Hz',
     'Vivobook 15 Intel Core 5 120 16GB 1TB SSD W11P 15.6" FHD Bilgisayar Csrtech',
     'Vivobook Go 15 E1504FA-BQ1741 AMD R5-7520U 8GB LPDDR5 512GB SSD 15.6″ Full HD 60Hz FreeDos',
     'TUF Gaming F16 FX608JM-RV075 8GB GeForce RTX5060 i5-13450HX 16GB RAM 512GB SSD 16" FHD+ 165Hz',
     'TUF Gaming A16 FA607NUG-RL211 6GB RTX4050 140w AMD Ryzen 7 7445HS 16GB 512GB SSD 16" FHD+ 144Hz',
     'TUF Gaming F16 FX607VJ Gaming Intel Core 5-210H 16GB 512GB SSD RTX3050 6GB 16 inç WUXGA 1',
     'TUF Gaming A15 FA506NCG-HN206-Gaming AMD Ryzen 7 7445HS 16GB 512GB SSD RTX 3050 15.6" FHD IPS Fdos',
     'Vivobook 15 13.Nesil Core i5 13420H-8Gb-512Gb Ssd-15.6inc-W11',
     '15.6-inch, FHD (1920 x 1080) 16:9 aspect ratio, 60Hz refresh rate, AMD Ryzen™ 5 7520u, Lpddr5 8',
     'E510KA-EJ881W Vivobook Go 15/Intel Celeron N4500/4 GB RAM/128 GB SSD/15.6"/W11 Laptop',
     'Vivobook 16 X1607QA-MB085W/ Snapdragon X1/ 16 GB Ram/ 512 GB SSD/ 16"/ W11 Laptop Soğuk Gümüş',
     'TUF Gaming A16 FA607NUG-RL212 R7 7445HS 16GB 512GB SSD RTX4050-6GB 140W Dos 16" WUXGA 144Hz Notebook',
     'TUF A16 FA607NUG-RL125-Gaming AMD Ryzen 7 7445HS 16GB 512GB SSD RTX 4050 6GB 16" FHD+ WUXGA IPS Fdos',
     'Vivobook 15 Intel Core 5 120U 8GB 512GB SSD Windows 11 Home 15.6'' FHD X1504VA-NJ3663W']
    

def test_extract_series():
   for i,e in enumerate(test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted series: {extract_series(e)}")
        print()

def test_cpu_extraction():
    for i,e in enumerate(test_asus_cases):
        print(f"Test case {i}: {e}")
        print(f"Extracted CPU: {extract_cpu(e)}")
        print()

if __name__ == "__main__":
    test_cpu_extraction()