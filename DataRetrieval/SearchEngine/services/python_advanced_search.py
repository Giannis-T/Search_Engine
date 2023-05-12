
import gensim.downloader as api
import gensim
import pandas as pd
from nltk.corpus import stopwords
import numpy as np
from gensim import utils
from scipy.spatial.distance import cdist
import os
import re

stop_words = stopwords.words('english')
g_model = gensim.models.KeyedVectors.load_word2vec_format("C:/Users/Giannis/gensim-data/word2vec-google-news-300/GoogleNews-vectors-negative300.bin", binary=True)  

def preprocess_lyrics(df):
    df["lyrics"] = [" ".join(utils.simple_preprocess(x)) for x in df["lyrics"]]
    return df

def encode_lyrics(df):
    embeddings = []
    for lyrics in df["lyrics"]:
        embedding = []
        for word in lyrics.split():
            try:
                embedding.append(g_model[word])
            except KeyError:
                pass
        embeddings.append(np.mean(embedding, axis=0))
    return np.array(embeddings)

def save_encoded_df(df, filename):
    np.save(filename, encode_lyrics(preprocess_lyrics(df)))

def load_encoded_df(filename):
    return np.load(filename)

def find_similar_songs(query, encoded_df, df, page_number):
    if len(query) == 1:
        query += " a"
    df_query = pd.DataFrame({"lyrics": [query]})
    query_embedding = preprocess_lyrics(df_query)
    query_embedding = encode_lyrics(query_embedding)
    distances= cdist(encoded_df, query_embedding)
    smallest_distances = np.argsort(distances.T)[0][((page_number-1)*10):(page_number*10)]
    results = [] 
    for distance in smallest_distances:
        results.append(df.iloc[distance])
    return results

def highlight_words(query, lyric):
    for word in query.split():
        if word != "a":
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            lyric = pattern.sub(r'<b>\g<0></b>', lyric)
    return lyric

def python_advanced_search(query, page_number):
    encoded_df = load_encoded_df(".\SearchEngine\services\encoded_data.npy") 
    
    df = pd.read_csv("C:/Users/Giannis/Desktop/SearchEngine/data/clean_songs.tsv", sep="\t")
    results = find_similar_songs(query, encoded_df, df, page_number)

    results_dict = {"artist":[], "title":[], "lyrics":[]}
    for result in results:
        results_dict["artist"].append(result["artist"])
        results_dict["title"].append(result["title"])
        results_dict["lyrics"].append(highlight_words(query, result["lyrics"]))

    df_results = pd.DataFrame(results_dict)
    return df_results

# print(python_advanced_search("waterloo"))


