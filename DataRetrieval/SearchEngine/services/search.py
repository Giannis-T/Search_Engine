import subprocess
import os
import pandas as pd
from .process_output import process_output

def java_search(query, field):
    output = subprocess.run(f"java -cp search_app.jar SearchModule {query} {field}", capture_output=True, cwd="C:/Users/Giannis/Desktop/SearchEngine/DataRetrieval/SearchEngine/services")
    return process_output(str(output))

    	
