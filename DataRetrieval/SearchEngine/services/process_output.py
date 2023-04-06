import pandas as pd
import subprocess
import os
import numpy as np

def process_output(output):
    if output == "Empty":
        return pd.DataFrame()
    lines = output.split("###")[1:]
    result = []
    for line in lines:
        line = line[:-4].split("$$$")
        tmp = []
        for word in line:
            tmp.append(word.replace('\\', ''))

        result.append(tmp)

    result = np.array(result)
    
    df = pd.DataFrame(result, columns=["rank", "artist", "title", "lyrics"])
    df.set_index(df["rank"].astype(int), inplace=True)
    df = df[["artist", "title", "lyrics"]]
    df.at[len(df),'lyrics'] = df.at[len(df),'lyrics'][:-8]
    df.drop_duplicates(subset="lyrics", inplace=True)
    return df