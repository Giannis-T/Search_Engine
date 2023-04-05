import subprocess
import os
import pandas as pd
from .process_output import process_output

def java_search(query, field):
    if field in {"artist", "song", "text"}:
        output = subprocess.run(f"java -cp search_app.jar SearchModule {query} {field}", capture_output=True, cwd="C:/Users/Giannis/Desktop/SearchEngine/DataRetrieval/SearchEngine/services")
        return process_output(str(output))
    else:
        return process_output("Empty")
# C:\Users\Giannis\Desktop\Eclipse_Projects\eclipse-workspace\SearchEngine\src\HelloLucene.java

    	
