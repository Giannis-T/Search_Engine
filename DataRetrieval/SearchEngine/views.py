from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
import json
from .services.search import java_search

# Create your views here.
results = pd.read_csv("..\data\clean_songs.csv")

def index(request):
    return HttpResponseRedirect("search")
    # output = java_search("Giannis")
    # return HttpResponse(output)

def search(request):
    return render(request,"search_engine/search.html")

def view_history(request):
    return render(request,"search_engine/view_history.html")

def view_results(request):
    json_records = results[0:3].reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    # return HttpResponse(results[0:10])
    return render(request, "search_engine/view_results.html", {
        "results": data
    })  

def next_ten():
    pass

def advanced_search(request):
    return render(request,"search_engine/advanced_search.html")