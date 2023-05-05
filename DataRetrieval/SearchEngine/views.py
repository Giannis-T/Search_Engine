from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponseRedirect
import json
from .services.search import java_search
from .models import Query


global current_page
current_page = 1

def index(request):
    return HttpResponseRedirect("search")

def search(request, history_query_id=-1):
    global current_page
    current_page = 1
    if request.method == "POST" or history_query_id != -1:
        query_response = request.POST.get("q")
        if query_response == "":
            return HttpResponseRedirect(reverse("search"))
        if history_query_id == -1 :
            query = query_response.split()[0]
            field = request.POST.get("field")
        else:
            history_query = Query.objects.get(pk=history_query_id)
            query = history_query.query
            field = history_query.field

        output = java_search(query, field, current_page)
        if not output.empty:
            Query.objects.create(query = query, field = field) 

            json_records = output.reset_index().to_json(orient ='records')
            data = json.loads(json_records)
            
            return render(request, "search_engine/view_results.html", {
                "results": data,
                "query":query,
                "field":field,
                "current_page":current_page,
            })
        
        return HttpResponseRedirect(reverse("search"))

    
    return render(request,"search_engine/search.html", {
        "fields":["artist", "title", "lyrics" ],
    })

def view_history(request):
    return render(request,"search_engine/view_history.html", {
        "history_queries": Query.objects.all()[::-1],
    })

def next_ten(request):
    global current_page
    query = request.POST.get("q")
    field = request.POST.get("field")

    output = java_search(query, field, current_page+1)
    current_page += 1
    if not output.empty:
        json_records = output.reset_index().to_json(orient ='records')
        data = json.loads(json_records)
        
        return render(request, "search_engine/view_results.html", {
            "results": data,
            "query":query,
            "field":field,
            "current_page":current_page,
        })
    return HttpResponseRedirect(reverse("search"))

def prev_ten(request):
    global current_page
    query = request.POST.get("q")
    field = request.POST.get("field")
    if current_page == 1:
        output = java_search(query, field, current_page)
    else:
        output = java_search(query, field, current_page-1)
        current_page -= 1
    if not output.empty:
        json_records = output.reset_index().to_json(orient ='records')
        data = json.loads(json_records)
        
        return render(request, "search_engine/view_results.html", {
            "results": data,
            "query":query,
            "field":field,
            "current_page":current_page,
        })
    return HttpResponseRedirect(reverse("search"))



def advanced_search(request):
    return render(request,"search_engine/advanced_search.html")