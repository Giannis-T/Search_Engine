import pandas as pd
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

def get_recommendation(history_queries_list):
    queries = ""
    queries_dict = {"pk":[], "query":[], "field":[]}
    for query in history_queries_list:
        queries_dict["pk"].append(query.pk)
        queries_dict["query"].append(query.query)
        queries_dict["field"].append(query.field)
    df = pd.DataFrame(queries_dict)
    df['query'] = df['query'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
    df = df.loc[df["query"] != ""]
    return (df["query"].value_counts().index[0], df["field"].value_counts().index[0])