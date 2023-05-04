from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
import json
from .services.search import java_search

current_page = 1

def index(request):
    return HttpResponseRedirect("search")

def search(request):
    if request.method == "POST":
        query_response = request.POST.get("q")
        if query_response == "":
            return HttpResponseRedirect(reverse("search"))
        
        query = query_response.split()[0]
        field = request.POST.get("field")
        output = java_search(query, field, current_page)
        if not output.empty:
            json_records = output.reset_index().to_json(orient ='records')
            data = json.loads(json_records)
            
            return render(request, "search_engine/view_results.html", {
                "results": data,
            })
        
        return HttpResponseRedirect(reverse("search"))

    
    return render(request,"search_engine/search.html", {
        "fields":["artist", "title", "lyrics" ],
    })

def view_history(request):
    return render(request,"search_engine/view_history.html", {
        "fields":["artist", "title", "lyrics" ],
    })

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