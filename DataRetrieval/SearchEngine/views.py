from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponseRedirect
import json
from .services.python_advanced_search import python_advanced_search
from .services.search import java_search
from .services.recommend_history_module import get_recommendation
from .services.group_by_artist import sort_results
from .models import Query
import gensim

global current_page
current_page = 1

def index(request):
    return HttpResponseRedirect("search")

def search(request, history_query_id=-1, rec_query="-", rec_field=""):
    global current_page
    current_page = 1

    if request.method == "POST" or history_query_id != -1 or rec_query != "-":
        query_response = request.POST.get("q")
        if query_response == "":
            return HttpResponseRedirect(reverse("search"))
        if rec_query != "-":
            query = rec_query
            field = rec_field

        elif history_query_id == -1 :
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
                "search_type": "search",
            })
        print("Empty Output")
        return HttpResponseRedirect(reverse("search"))

    
    return render(request,"search_engine/search.html", {
        "fields":["artist", "title", "lyrics" ],
    })

def view_history(request):
    try:
        recommendation = get_recommendation(Query.objects.all())
    except:
        recommendation = ("", "")
    return render(request,"search_engine/view_history.html", {
        "history_queries": Query.objects.all()[::-1],
        "rec_query": recommendation[0],
        "rec_field": recommendation[1],
    })

def delete_history(request):
    Query.objects.all().delete()
    print("Successful Deletion")
    return HttpResponseRedirect("view_history")

def next_ten(request):
    global current_page
    query = request.POST.get("q")
    field = request.POST.get("field")
    search_type = request.POST.get("search_type")

    if search_type == "advanced_search":
        output = python_advanced_search(query, current_page+1)
    else:
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
            "search_type":search_type,
        })
    return HttpResponseRedirect(reverse("search"))

def prev_ten(request):
    global current_page
    query = request.POST.get("q")
    field = request.POST.get("field")
    search_type = request.POST.get("search_type")

    if current_page == 1:
        if search_type == "advanced_search":
            output = python_advanced_search(query, current_page)
        else:
            output = java_search(query, field, current_page)
    else:
        if search_type == "advanced_search":
            output = python_advanced_search(query, current_page-1)
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
            "search_type":search_type,
        })
    return HttpResponseRedirect(reverse("search"))


def group_by_len(request):
    global current_page
    if request.method == "POST":
        query = request.POST.get("q")
        field = request.POST.get("field")
        result = java_search(query, field, current_page)
        if not result.empty:
            output = sort_results(result)
            json_records = output.reset_index().to_json(orient ='records')
            data = json.loads(json_records)
            
            return render(request, "search_engine/view_results.html", {
                "results": data,
                "query":query,
                "field":field,
                "current_page":current_page,
            })
        return HttpResponseRedirect(reverse("search"))

    return HttpResponseRedirect(reverse("search"))


def advanced_search(request):
    global current_page
    current_page = 1
    if request.method == "POST":
        query = request.POST.get("q")
        if query == "":
            return HttpResponseRedirect(reverse("search"))

        output = python_advanced_search(query, current_page)

        if not output.empty:
            Query.objects.create(query = query, field = "lyrics") 

            json_records = output.reset_index().to_json(orient ='records')
            data = json.loads(json_records)
            
            return render(request, "search_engine/view_results.html", {
                "results": data,
                "query":query,
                "field":"lyrics",
                "current_page":current_page,
                "search_type": "advanced_search",

            })
        print("Empty Output")
        return HttpResponseRedirect(reverse("advanced_search"))
    
    return render(request,"search_engine/advanced_search.html", {
        "fields":["artist", "title", "lyrics" ],
    })
