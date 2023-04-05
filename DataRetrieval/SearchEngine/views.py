from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
import json
from .services.search import java_search


def index(request):
    return HttpResponseRedirect("search")

def search(request):
    if request.method == "POST":
        response = request.POST.get("q").split()
        query = response[0]
        if len(response) > 1:
            field = response[1]
        output = java_search(query, field="text")
        if not output.empty:
            json_records = output.reset_index().to_json(orient ='records')
            data = json.loads(json_records)
            
            return render(request, "search_engine/view_results.html", {
                "results": data
            })
        
        return HttpResponseRedirect(reverse("search"))

    
    return render(request,"search_engine/search.html")

def view_history(request):
    return render(request,"search_engine/view_history.html")

# def view_results(request, results):
#     # json_records = results[0:3].reset_index().to_json(orient ='records')
#     # data = []
#     # data = json.loads(json_records)
#     return render(request, "search_engine/view_results.html", {
#         "results": results
#     })  

def next_ten():
    pass

def advanced_search(request):
    return render(request,"search_engine/advanced_search.html")