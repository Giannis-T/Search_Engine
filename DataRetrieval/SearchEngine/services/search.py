import subprocess
import os
import pandas as pd
from .process_output import process_output

def java_search(query, field, pageNumber=1):
    output = subprocess.run(f"java -cp search_app.jar SearchModule {query} {field} {pageNumber}", capture_output=True, cwd="C:/Users/Giannis/Desktop/SearchEngine/DataRetrieval/SearchEngine/services")
    return process_output(str(output))

    	
