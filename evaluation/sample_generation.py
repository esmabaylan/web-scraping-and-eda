import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd


import scripts.paths as paths
"""
This script creates a sample of the dataset for evaluation purposes.
arguments:
- input_file: The path to the input dataset file (CSV or JSON).
- golden_column: The name of the column in the dataset that contains the golden labels for the
    feature being evaluated (e.g., "cpu", "gpu", "ram", "os", "storage").
- sample_size: The number of samples to include in the output file (default is 1000).

The script reads the input dataset, randomly samples the specified number of rows, and creates a new CSV file containing the sampled data along with an empty column for manual labeling of the golden feature. 
The output file is saved in the evaluation directory with a name based on the golden column (e.g., "gpu_sample.csv"). 
This allows for easy manual annotation and evaluation of the extracted features against the golden labels.
"""

def create_sample_data(input_file ,golden_column,sample_size=1000):
    output_file =paths.EVAL_DIR +f"/sample_data/{golden_column}_sample.csv"
    if input_file.endswith(".json"):
        df = pd.read_json(input_file)
    elif input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    else:
        raise ValueError("Unsupported file format. Please provide a .json or .csv file.")
    sample_df = df.sample(n=sample_size, random_state=42)
    sample_df.drop(columns=["brand","reviews","link","rating","price"],inplace=True)
    sample_df[f"manual_{golden_column}"]=""
    sample_df.to_csv(output_file, index=False)
    print(f"Sample of {sample_size} rows created and saved to {output_file}")

if __name__ == "__main__":
    features = ["cpu","gpu","ram","os","storage"]
    for feature in features:
        if feature == "gpu":
            create_sample_data(paths.DATA_DIR + "/raw/dataset.json", feature, 1000)
