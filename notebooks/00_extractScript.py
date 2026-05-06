import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import scripts.extract_features as extract_features

import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

df=pd.read_json("./data/raw/dataset.json")

def preview(df):
    print("Dataframe shape:", df.shape)
    print("\nDataframe info:")
    print(df.info())
    print("\nDataframe columns:", df.columns)
    print("\nDataframe unique values count:")
    for colmn in df.columns:
        print(f"{colmn}: {df[colmn].nunique()}")


preview(df)

df["price"]=df["price"].str.replace("TL","").str.replace(".","").str.replace(",",".").astype(float)
df["rating"]=df["rating"].astype(float)
df["reviews"]=df["reviews"].astype(int)
df["link"]=df["link"].astype(object)
df["brand"]=df["brand"].astype(object)

df.drop(columns=["reviews","link","rating"], inplace=True)
print(df.info())

extract_features_df=df["name"].apply(
    extract_features.get_features_parallel).apply(pd.Series)
extract_features_df=pd.concat([df, extract_features_df], axis=1)

extract_features_df.to_csv("./data/processed/extracted_features.csv", index=False)
