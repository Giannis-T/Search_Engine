import pandas as pd
import numpy as np

def process_output(output):
    if "Found 0 hits" in output:
        print("Empty Dataframe")
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
    print("_________________________IM IN Process OUTPUT_______________________")
    

    df = pd.DataFrame(result, columns=["rank", "artist", "title", "lyrics"])
    df.set_index(df["rank"].astype(int), inplace=True)
    df = df[["artist", "title", "lyrics"]]
    df.loc[df.index[-1], 'lyrics'] = df.loc[df.index[-1], 'lyrics'][:-10]
    return df