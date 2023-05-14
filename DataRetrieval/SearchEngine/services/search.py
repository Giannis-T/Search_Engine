import subprocess
from .process_output import process_output

def java_search(query, field, page_number=1):
    output = subprocess.run(f"java -cp search_app.jar SearchModule {query} {field} {page_number}", capture_output=True, cwd="C:/Users/Giannis/Desktop/SearchEngine/DataRetrieval/SearchEngine/services")
    return process_output(str(output))

    	
