
# Trendyol Laptop Data Analysis

An automated pipeline that scrapes laptop prices and specifications from Trendyol using Puppeteer and performs exploratory data analysis using Python.

## Features

- **Targeted Scraping**: Collects data from specific major brands including Asus, Lenovo, HP, Apple, Dell, Monster, MSI, Casper, Acer, and Huawei.
- **Concurrency**: Optimized performance with concurrent page scraping (10 requests per brand) to avoid rate limits.
- **Data Extraction**: Parses unstructured product titles to extract key features like Processor, RAM, GPU, and Storage.
- **Output**: Generates a structured JSON dataset ready for analysis.

## Technologies

- **Scraping**: Node.js, Puppeteer
- **Analysis**: Python, Pandas, NumPy, Jupyter Notebook

## Installation

1. Install Node.js dependencies:
   ```bash
   npm install
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

**1. Run the Scraper**
Start the data collection process. This will generate `trendyol_full_dataset.json`.

```bash
node scraper.js

```

**2. Run Analysis**
Open the Jupyter Notebook to visualize and analyze the gathered data.

```bash
jupyter notebook notebooks/00_datapreview.ipynb

```

**3. Test Feature Extraction**
Verify the text processing logic used for specification extraction.

```bash
python scripts/test.py

```