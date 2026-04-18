import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd


import scripts.paths as paths
def create_sample_gpu_data(input_file,output_file =paths.EVAL_DIR + "/gpu_sample.csv"
                           ,sample_size=1000):
    if input_file.endswith(".json"):
        df = pd.read_json(input_file)
    elif input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    else:
        raise ValueError("Unsupported file format. Please provide a .json or .csv file.")
    sample_df = df.sample(n=sample_size, random_state=42)
    sample_df.drop(columns=["brand","reviews","link","rating","price"],inplace=True)
    sample_df["manual_gpu"]=""
    sample_df.to_csv(output_file, index=False)
    print(f"Sample of {sample_size} rows created and saved to {output_file}")

if __name__ == "__main__":
    create_sample_gpu_data(paths.DATA_DIR + "/raw/dataset.json")