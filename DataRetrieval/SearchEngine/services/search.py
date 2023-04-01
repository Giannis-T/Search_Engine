import subprocess
import os
def java_search(query):
    # output = subprocess.run(f"java SearchModule {query}", capture_output=True, cwd="C:\Users\Giannis\Desktop\Eclipse_Projects\eclipse-workspace\SearchEngine\src")
    # print(output.stdout)
    # results = ""
    # print(output)
    # cwd = os.getcwd()  # Get the current working directory (cwd)
    # files = os.listdir(cwd)  # Get all the files in that directory
    # print("Files in %r: %s" % (cwd, files))
    # f = open("SearchEngine/services/results.txt", "r")
    # results = f.read()       
    # f.close()
    output = subprocess.run(f"java -cp search_app.jar HelloLucene", capture_output=True, cwd="C:/Users/Giannis/Desktop/SearchEngine/DataRetrieval/SearchEngine/services")
    print(output.stdout)

    # output = subprocess.run(f"java SearchModule {query}", capture_output=True, cwd="C:/Users/Giannis/Desktop/SearchEngine/DataRetrieval/SearchEngine/services")
    # print(output.stdout)
    with open("SearchEngine/services/results.txt", "r") as f:
        results = f.read()
    # print(output)
    return results
# C:\Users\Giannis\Desktop\Eclipse_Projects\eclipse-workspace\SearchEngine\src\HelloLucene.java

    	
