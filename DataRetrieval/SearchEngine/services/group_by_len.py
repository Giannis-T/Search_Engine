import pandas as pd

def sort_results(df):
    res = df["lyrics"].str.len().sort_values().index
    df = df.reindex(res)
    return df